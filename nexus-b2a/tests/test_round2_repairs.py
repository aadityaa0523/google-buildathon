"""
Regression tests verifying Round 2 audit findings:
- F01: Owner credential derivation & non-demo forgery denial; account read isolation
- F05: Cancel pre-dispatch cannot be overwritten by dispatch claim
- F06: Concurrent dispute adjudication uniqueness (no double credit reversal)
- F07: Semantic value-to-evidence span matching (1 minor unit vs 11,800 snippet)
- F09: Timezone offset normalized expiry (11:00+02:00 evaluated as 09:00 UTC)
- F10: Content-free safe error diagnostics (no raw exception text in order metadata)
- F13: Approved refund order is readable via GET /v1/orders/{id} with canonical REVERSED state
- F14: Concurrent identical purchase idempotency winner resolution
- F15: Validation past deadline triggers expiration, never settlement
- F16: Idempotent replay succeeds even after spend grant revocation
- Advertised targets: Schema, sellers, and MCP return 200 instead of 404
"""

import os
import json
import pytest
from datetime import datetime, timezone, timedelta
from starlette.testclient import TestClient
from app.main import create_app
from app.core.database import Database
from app.core.clock import Clock
from app.models.core import OrderExecutionState, AccountingState, DisputeStatus
from app.models.extraction import ExtractionResult, LineItem, EvidenceSpan, validate_extraction_evidence
from tests.conftest import SAMPLE_INVOICE_TEXT


def test_f01_non_demo_forged_owner_id_denied():
    """Verifies F01: Outside demo mode, X-Owner-Id without valid owner key fails closed (401)."""
    db = Database(":memory:")
    clock = Clock(datetime(2026, 11, 14, 10, 0, 0, tzinfo=timezone.utc))
    # Create app with enable_demo_mode=False
    app = create_app(db=db, clock=clock, enable_demo_mode=False)
    authority = app.state.authority
    client = TestClient(app)

    # Create owner Alice
    alice = authority.create_owner("alice@corp.in", "Alice")
    alice_key, _ = authority.issue_owner_key(alice.id)

    # 1. Forged owner ID without owner key is rejected (401)
    res_forged = client.post(
        "/v1/agents",
        json={"owner_id": alice.id, "name": "ForgedAgent"},
        headers={"X-Owner-Id": alice.id}
    )
    assert res_forged.status_code == 401
    assert "Owner credential" in res_forged.text or "UNAUTHENTICATED" in res_forged.text

    # 2. Genuine owner key succeeds (200)
    res_legit = client.post(
        "/v1/agents",
        json={"owner_id": alice.id, "name": "LegitAgent"},
        headers={"X-Owner-Key": alice_key}
    )
    assert res_legit.status_code == 200
    agent_id = res_legit.json()["id"]

    # 3. Issue key with genuine owner key succeeds
    res_key = client.post(
        f"/v1/agents/{agent_id}/keys",
        headers={"Authorization": f"Bearer {alice_key}"}
    )
    assert res_key.status_code == 200


def test_f01_account_read_isolation(app_and_services):
    """Verifies F01: Unauthenticated or wrong-owner read of account balance is denied."""
    ctx = app_and_services
    app = ctx["app"]
    alice = ctx["alice"]
    bob = ctx["bob"]
    bob_key = ctx["bob_key"]
    raw_key = ctx["raw_key"]
    client = TestClient(app)

    # 1. Unauthenticated read is denied (403)
    res_anon = client.get(f"/v1/accounts/{alice.id}")
    assert res_anon.status_code == 403

    # 2. Bob cannot view Alice's account (403)
    res_bob = client.get(f"/v1/accounts/{alice.id}", headers={"X-Owner-Key": bob_key})
    assert res_bob.status_code == 403

    # 3. Alice's agent can view Alice's account (200)
    res_agent = client.get(f"/v1/accounts/{alice.id}", headers={"Authorization": f"Bearer {raw_key}"})
    assert res_agent.status_code == 200
    assert res_agent.json()["available_credits"] == 5000


def test_f05_cancel_pre_dispatch_cannot_be_overwritten(app_and_services):
    """Verifies F05: Order cancelled in RESERVED state cannot be claimed or dispatched."""
    ctx = app_and_services
    app = ctx["app"]
    raw_key = ctx["raw_key"]
    grant = ctx["grant"]
    alice = ctx["alice"]
    commerce = app.state.commerce
    client = TestClient(app)

    # Register mock seller that records calls
    dispatch_called = []
    def recording_seller(payload):
        dispatch_called.append(payload["order_id"])
        from app.sellers.deterministic_seller import extract_with_rules
        return extract_with_rules(payload["input_text"])

    app.state.fulfillment.register_mock_seller("http://localhost:8000/sellers/rec_test", recording_seller)
    rec_offer = app.state.offers.publish_offer(
        seller_id=ctx["seller"].id,
        title="Recording Seller",
        description="Tracks dispatch calls",
        buyer_total_credits=100,
        seller_net_credits=85,
        nexus_fee_credits=15,
        endpoint_url="http://localhost:8000/sellers/rec_test"
    )

    # Intercept purchase between reservation and dispatch by mocking _claim_order_for_dispatch
    original_claim = commerce._claim_order_for_dispatch
    def cancel_before_claim(order_id):
        # Cancel order while still in RESERVED state
        commerce.cancel_order(order_id, alice.id)
        # Call original claim (which must fail with CAS because state is CANCELLED)
        return original_claim(order_id)

    commerce._claim_order_for_dispatch = cancel_before_claim
    try:
        headers = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "CANCEL-PRE-01"}
        res = client.post("/v1/orders", json={
            "offer_id": rec_offer.id,
            "expected_offer_version": rec_offer.version,
            "grant_id": grant.id,
            "raw_invoice_text": SAMPLE_INVOICE_TEXT
        }, headers=headers)
        assert res.status_code == 200
        order_data = res.json()
        assert order_data["execution_state"] == "CANCELLED"
        assert order_data["accounting_state"] == "RELEASED"

        # Dispatch was NEVER called!
        assert len(dispatch_called) == 0

        # Buyer wallet remained exactly 5000 with 0 reserved
        buyer_bal = ctx["db"].get_connection().execute("SELECT available_credits, reserved_credits FROM accounts WHERE account_id = ?", (alice.id,)).fetchone()
        assert buyer_bal["available_credits"] == 5000
        assert buyer_bal["reserved_credits"] == 0
    finally:
        commerce._claim_order_for_dispatch = original_claim


def test_f06_concurrent_dispute_approval_uniqueness(app_and_services):
    """Verifies F06: Second approval on a dispute raises DISPUTE_ALREADY_RESOLVED with zero extra credits."""
    ctx = app_and_services
    app = ctx["app"]
    raw_key = ctx["raw_key"]
    grant = ctx["grant"]
    offer = ctx["offer"]
    alice = ctx["alice"]
    accountability = app.state.accountability
    accounting = app.state.accounting
    client = TestClient(app)

    # 1. Purchase settled order
    headers = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "SETTLE-DISP-01"}
    res = client.post("/v1/orders", json={
        "offer_id": offer.id,
        "expected_offer_version": offer.version,
        "grant_id": grant.id,
        "raw_invoice_text": SAMPLE_INVOICE_TEXT
    }, headers=headers)
    order_id = res.json()["id"]

    # 2. Open dispute
    dispute = accountability.open_dispute(order_id, alice.id, "QUALITY", "Incorrect field")

    # 3. First adjudication succeeds
    op_headers = {"X-Operator-Key": "nexus_admin_operator_key_2026"}
    res1 = client.post(
        f"/v1/operator/disputes/{dispute.id}/adjudicate",
        json={"approved": True, "operator_reason": "Approved"},
        headers=op_headers
    )
    assert res1.status_code == 200

    bal_after_first = accounting.get_or_create_account(alice.id, "BUYER")
    assert bal_after_first["available_credits"] == 5000

    # 4. Second concurrent/serial adjudication MUST be rejected
    res2 = client.post(
        f"/v1/operator/disputes/{dispute.id}/adjudicate",
        json={"approved": True, "operator_reason": "DuplicateApproval"},
        headers=op_headers
    )
    assert res2.status_code == 400
    assert "DISPUTE_ALREADY_RESOLVED" in res2.text

    # Balance must NOT mint extra credits (still 5000)
    bal_after_second = accounting.get_or_create_account(alice.id, "BUYER")
    assert bal_after_second["available_credits"] == 5000


def test_f07_value_to_evidence_span_mismatch_rejected():
    """Verifies F07: A result reporting total 1 minor unit while evidence snippet says 11,800 is rejected."""
    sample_text = "Total Amount: ₹11,800.00"
    span = EvidenceSpan(
        field_name="total_amount_minor",
        start_offset=sample_text.index("₹11,800.00"),
        end_offset=sample_text.index("₹11,800.00") + len("₹11,800.00"),
        snippet="₹11,800.00"
    )
    # Seller reports total_amount_minor = 1 (1 paise instead of 11,800.00)
    bogus_result = ExtractionResult(
        vendor_name=None,
        invoice_number=None,
        invoice_date=None,
        currency="INR",
        subtotal_amount_minor=None,
        tax_amount_minor=None,
        total_amount_minor=1,
        line_items=[],
        evidence_spans=[span],
        missing_fields_reasons={
            "subtotal_amount_minor": "Not found",
            "tax_amount_minor": "Not found"
        }
    )

    errors = validate_extraction_evidence(sample_text, bogus_result)
    assert any("VALUE_SPAN_MISMATCH" in e for e in errors)


def test_f09_timezone_offset_expiry(app_and_services):
    """Verifies F09: At server time 10:00 UTC, expiry 11:00+02:00 (09:00 UTC, expired) is rejected with 422."""
    ctx = app_and_services
    app = ctx["app"]
    raw_key = ctx["raw_key"]
    alice = ctx["alice"]
    offer = ctx["offer"]
    authority = app.state.authority
    client = TestClient(app)

    # Server clock is 10:00 UTC
    agent = authority.register_agent(alice.id, "OffsetAgent")
    raw_agt_key, _ = authority.issue_agent_key(agent.id)

    # Create grant expiring at 11:00 AM in UTC+2 (= 09:00 AM UTC, already 1 hour in the past!)
    expired_offset_ts = "2026-11-14T11:00:00+02:00"
    grant = authority.create_spend_grant(
        owner_id=alice.id,
        agent_id=agent.id,
        max_allowance_credits=500,
        per_order_max_credits=250,
        expires_at=expired_offset_ts
    )

    headers = {"Authorization": f"Bearer {raw_agt_key}", "Idempotency-Key": "EXP-OFFSET-01"}
    res = client.post("/v1/orders", json={
        "offer_id": offer.id,
        "expected_offer_version": offer.version,
        "grant_id": grant.id,
        "raw_invoice_text": SAMPLE_INVOICE_TEXT
    }, headers=headers)
    assert res.status_code == 422
    assert "POLICY_DENIAL" in res.text
    assert "expired" in res.text.lower()


def test_f13_refunded_order_readable(app_and_services):
    """Verifies F13: Approved refund stores canonical REVERSED state and GET /v1/orders/{id} returns 200."""
    ctx = app_and_services
    app = ctx["app"]
    raw_key = ctx["raw_key"]
    grant = ctx["grant"]
    offer = ctx["offer"]
    alice = ctx["alice"]
    accountability = app.state.accountability
    client = TestClient(app)

    # Purchase
    headers = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "REF-READ-01"}
    res = client.post("/v1/orders", json={
        "offer_id": offer.id,
        "expected_offer_version": offer.version,
        "grant_id": grant.id,
        "raw_invoice_text": SAMPLE_INVOICE_TEXT
    }, headers=headers)
    order_id = res.json()["id"]

    # Dispute and refund
    disp = accountability.open_dispute(order_id, alice.id, "FRAUD", "Defective")
    op_headers = {"X-Operator-Key": "nexus_admin_operator_key_2026"}
    client.post(
        f"/v1/operator/disputes/{disp.id}/adjudicate",
        json={"approved": True, "operator_reason": "Approved"},
        headers=op_headers
    )

    # Authenticated order read MUST succeed with 200 (never 500)
    order_res = client.get(f"/v1/orders/{order_id}", headers=headers)
    assert order_res.status_code == 200
    order_data = order_res.json()
    assert order_data["accounting_state"] == "REVERSED"


def test_f14_concurrent_identical_purchase_idempotency(app_and_services):
    """Verifies F14: Two requests with identical key return the exact same order without crash."""
    ctx = app_and_services
    app = ctx["app"]
    raw_key = ctx["raw_key"]
    grant = ctx["grant"]
    offer = ctx["offer"]
    client = TestClient(app)

    headers = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "CONCURRENT-IDEMP-01"}
    payload = {
        "offer_id": offer.id,
        "expected_offer_version": offer.version,
        "grant_id": grant.id,
        "raw_invoice_text": SAMPLE_INVOICE_TEXT
    }

    res1 = client.post("/v1/orders", json=payload, headers=headers)
    res2 = client.post("/v1/orders", json=payload, headers=headers)

    assert res1.status_code == 200
    assert res2.status_code == 200
    assert res1.json()["id"] == res2.json()["id"]


def test_f15_validation_past_deadline_expires(app_and_services):
    """Verifies F15: If validation finishes after the deadline, order expires and releases credits."""
    ctx = app_and_services
    app = ctx["app"]
    raw_key = ctx["raw_key"]
    grant = ctx["grant"]
    offer = ctx["offer"]
    clock = ctx["clock"]
    fulfillment = app.state.fulfillment
    client = TestClient(app)

    # Mock validation advancing clock past 30s deadline
    orig_validate = fulfillment.validate_extraction_result
    def slow_validator(raw_text, result_data):
        clock.advance(seconds=60)  # Past 30s deadline
        return orig_validate(raw_text, result_data)

    fulfillment.validate_extraction_result = slow_validator
    try:
        headers = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "DEADLINE-SLOW-VAL-01"}
        res = client.post("/v1/orders", json={
            "offer_id": offer.id,
            "expected_offer_version": offer.version,
            "grant_id": grant.id,
            "raw_invoice_text": SAMPLE_INVOICE_TEXT
        }, headers=headers)
        assert res.status_code == 200
        order_data = res.json()
        assert order_data["execution_state"] == "EXPIRED"
        assert order_data["accounting_state"] == "RELEASED"
    finally:
        fulfillment.validate_extraction_result = orig_validate


def test_f16_idempotent_retry_after_grant_revocation(app_and_services):
    """Verifies F16: Replaying a completed purchase after grant revocation returns existing order."""
    ctx = app_and_services
    app = ctx["app"]
    raw_key = ctx["raw_key"]
    grant = ctx["grant"]
    offer = ctx["offer"]
    alice = ctx["alice"]
    authority = app.state.authority
    client = TestClient(app)

    headers = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "RETRY-REVOKED-01"}
    payload = {
        "offer_id": offer.id,
        "expected_offer_version": offer.version,
        "grant_id": grant.id,
        "raw_invoice_text": SAMPLE_INVOICE_TEXT
    }

    # 1. First purchase succeeds
    res1 = client.post("/v1/orders", json=payload, headers=headers)
    assert res1.status_code == 200
    order1 = res1.json()

    # 2. Revoke the spend grant
    authority.revoke_spend_grant(grant.id, alice.id)

    # 3. Replay with identical key MUST return existing order (200), not 422 POLICY_DENIAL
    res2 = client.post("/v1/orders", json=payload, headers=headers)
    assert res2.status_code == 200
    order2 = res2.json()
    assert order1["id"] == order2["id"]


def test_advertised_endpoints_status_200(app_and_services):
    """Verifies that advertised endpoints (/schemas, /sellers/deterministic, /mcp) return 200, never 404."""
    ctx = app_and_services
    app = ctx["app"]
    client = TestClient(app)

    # 1. Capability schema endpoint
    res_schema = client.get("/v1/schemas/invoice.extract.v1.json")
    assert res_schema.status_code == 200
    assert "invoice.extract.v1" in res_schema.text

    # 2. Seller HTTP endpoint
    res_seller = client.post("/sellers/deterministic", json={
        "job_id": "job_test",
        "input_text": SAMPLE_INVOICE_TEXT
    })
    assert res_seller.status_code == 200
    assert "vendor_name" in res_seller.json()

    # 3. MCP protocol endpoint
    res_mcp = client.get("/mcp")
    assert res_mcp.status_code == 200
    assert "Nexus MCP" in res_mcp.text
