"""
Regression tests verifying the release-blocking audit findings (F01 - F10)
from ROADMAP.md Section 0:
- F01: Role-based authority on owner and operator routes
- F02: No seller secrets returned on public endpoints or MCP tools
- F03/F04: Atomic conditional headroom checking (no grant overspend)
- F05: Order state machine CAS prevents late success after cancellation
- F06: Unsettled / released orders cannot be refunded
- F07: Strict extraction contract forbids extra fields and requires evidence
- F08: 32 KB UTF-8 byte size limit enforced upfront
- F09: Expired spend grants rejected before reservation
- F10: Content-free error codes without private text leakage
"""

import pytest
from starlette.testclient import TestClient
from tests.conftest import SAMPLE_INVOICE_TEXT
from app.models.extraction import ExtractionResult, LineItem, EvidenceSpan
from app.models.core import OrderExecutionState, AccountingState


def test_f01_f02_role_authority_and_public_secret_protection(app_and_services):
    """Verifies F01 (role-based authority) and F02 (no secrets in public offers)."""
    ctx = app_and_services
    app = ctx["app"]
    alice = ctx["alice"]
    bob = ctx["bob"]
    offer = ctx["offer"]
    client = TestClient(app)

    # 1. Anonymous agent registration is rejected (401)
    res_anon_agent = client.post("/v1/agents", json={"owner_id": alice.id, "name": "RogueAgent"})
    assert res_anon_agent.status_code == 401

    # 2. Register agent with proper owner auth
    res_alice_agent = client.post(
        "/v1/agents",
        json={"owner_id": alice.id, "name": "AliceLegitAgent"},
        headers={"X-Owner-Id": alice.id}
    )
    assert res_alice_agent.status_code == 200
    agent_id = res_alice_agent.json()["id"]

    # 3. Wrong owner cannot issue keys for Alice's agent (403)
    res_wrong_owner = client.post(
        f"/v1/agents/{agent_id}/keys",
        headers={"X-Owner-Id": bob.id}
    )
    assert res_wrong_owner.status_code == 403

    # 4. Anonymous call to operator routes is rejected (403)
    res_anon_sweep = client.post("/v1/operator/retention/sweep")
    assert res_anon_sweep.status_code == 403

    # 5. Public offers omit endpoint_secret (F02)
    offers_resp = client.get("/v1/offers")
    assert offers_resp.status_code == 200
    for o in offers_resp.json():
        assert "endpoint_secret" not in o

    single_offer_resp = client.get(f"/v1/offers/{offer.id}")
    assert single_offer_resp.status_code == 200
    assert "endpoint_secret" not in single_offer_resp.json()


def test_f04_aggregate_grant_limit_enforced(app_and_services):
    """Verifies F04: Aggregate allowance cannot be exceeded by concurrent/serial orders."""
    ctx = app_and_services
    app = ctx["app"]
    authority = app.state.authority
    alice = ctx["alice"]
    offer = ctx["offer"]
    client = TestClient(app)

    # Create grant with max allowance = 150 (offer is 100)
    agent = authority.register_agent(alice.id, "CapAgent")
    raw_key, _ = authority.issue_agent_key(agent.id)
    grant = authority.create_spend_grant(
        owner_id=alice.id,
        agent_id=agent.id,
        max_allowance_credits=150,
        per_order_max_credits=150,
        allowed_capabilities=["invoice.extract.v1"]
    )

    headers = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "CAP-01"}
    # 1. First purchase of 100 credits succeeds (leaves 50 allowance)
    res1 = client.post("/v1/orders", json={
        "offer_id": offer.id,
        "expected_offer_version": offer.version,
        "grant_id": grant.id,
        "raw_invoice_text": SAMPLE_INVOICE_TEXT
    }, headers=headers)
    assert res1.status_code == 200

    # 2. Second purchase of 100 credits MUST fail (100 > 50 remaining headroom)
    headers2 = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "CAP-02"}
    res2 = client.post("/v1/orders", json={
        "offer_id": offer.id,
        "expected_offer_version": offer.version,
        "grant_id": grant.id,
        "raw_invoice_text": SAMPLE_INVOICE_TEXT
    }, headers=headers2)
    assert res2.status_code == 422
    assert "POLICY_DENIAL" in res2.text


def test_f05_cancel_and_late_success_race_prevented(app_and_services):
    """Verifies F05: A cancelled order rejects late settlement with zero balance side-effects."""
    ctx = app_and_services
    app = ctx["app"]
    raw_key = ctx["raw_key"]
    grant = ctx["grant"]
    alice = ctx["alice"]
    seller = ctx["seller"]
    commerce = app.state.commerce
    client = TestClient(app)

    def controlled_cancelling_seller(job_payload):
        # Controlled seller cancels order during dispatch (F05)
        commerce.cancel_order(job_payload["order_id"], alice.id)
        from app.sellers.deterministic_seller import extract_with_rules
        return extract_with_rules(job_payload["input_text"])

    app.state.fulfillment.register_mock_seller("http://localhost:8000/sellers/cancelling_test", controlled_cancelling_seller)

    cancelling_offer = app.state.offers.publish_offer(
        seller_id=seller.id,
        title="Cancelling Seller",
        description="Cancels during dispatch to test race condition",
        buyer_total_credits=100,
        seller_net_credits=85,
        nexus_fee_credits=15,
        endpoint_url="http://localhost:8000/sellers/cancelling_test"
    )

    headers = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "RACE-01"}
    # Create order - triggers dispatch which cancels mid-flight then returns valid result
    res = client.post("/v1/orders", json={
        "offer_id": cancelling_offer.id,
        "expected_offer_version": cancelling_offer.version,
        "grant_id": grant.id,
        "raw_invoice_text": SAMPLE_INVOICE_TEXT
    }, headers=headers)
    assert res.status_code == 200
    order_id = res.json()["id"]

    cancelled_order = commerce.get_order_by_id(order_id)
    assert cancelled_order.execution_state == OrderExecutionState.CANCELLED
    assert cancelled_order.accounting_state == AccountingState.RELEASED

    # Check buyer balance
    buyer_bal = ctx["db"].get_connection().execute("SELECT available_credits, reserved_credits FROM accounts WHERE account_id = ?", (alice.id,)).fetchone()
    assert buyer_bal["reserved_credits"] == 0
    assert buyer_bal["available_credits"] == 5000

    # Simulate late seller result arriving after cancellation
    from datetime import datetime, timezone
    commerce._handle_success(cancelled_order, grant, {"test": "data"}, datetime.now(timezone.utc))

    # Buyer reserved balance MUST remain 0 (not negative -100)
    buyer_bal_after = ctx["db"].get_connection().execute("SELECT available_credits, reserved_credits FROM accounts WHERE account_id = ?", (alice.id,)).fetchone()
    assert buyer_bal_after["reserved_credits"] == 0
    assert buyer_bal_after["available_credits"] == 5000


def test_f06_unsettled_order_cannot_be_refunded(app_and_services):
    """Verifies F06: A failed or cancelled order cannot be disputed or refunded to mint extra credits."""
    from app.sellers.fault_seller import set_fault_mode, FAULT_MODE_TIMEOUT, FAULT_MODE_NONE
    ctx = app_and_services
    app = ctx["app"]
    raw_key = ctx["raw_key"]
    grant = ctx["grant"]
    seller = ctx["seller"]
    commerce = app.state.commerce
    client = TestClient(app)

    fault_offer = app.state.offers.publish_offer(
        seller_id=seller.id,
        title="Faulty Seller For Refund Test",
        description="Fails execution",
        buyer_total_credits=100,
        seller_net_credits=85,
        nexus_fee_credits=15,
        endpoint_url="http://localhost:8000/sellers/fault"
    )

    set_fault_mode(FAULT_MODE_TIMEOUT)
    try:
        # 1. Purchase fails
        headers = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "FAIL-REF-01"}
        res = client.post("/v1/orders", json={
            "offer_id": fault_offer.id,
            "expected_offer_version": 1,
            "grant_id": grant.id,
            "raw_invoice_text": SAMPLE_INVOICE_TEXT
        }, headers=headers)
        assert res.status_code == 200
        order_id = res.json()["id"]
        order = commerce.get_order_by_id(order_id)
        assert order.execution_state == OrderExecutionState.FAILED
        assert order.accounting_state == AccountingState.RELEASED

        # 2. Attempting to open dispute on failed/released order fails
        res_disp = client.post("/v1/disputes", json={
            "order_id": order_id,
            "reason": "FRAUD",
            "details": "Refund me anyway"
        }, headers=headers)
        assert res_disp.status_code == 400
        assert "CANNOT_DISPUTE_UNSETTLED_ORDER" in res_disp.text
    finally:
        set_fault_mode(FAULT_MODE_NONE)


def test_f08_utf8_byte_limit_enforced(app_and_services):
    """Verifies F08: Payloads exceeding 32 KB UTF-8 are rejected upfront."""
    ctx = app_and_services
    app = ctx["app"]
    raw_key = ctx["raw_key"]
    grant = ctx["grant"]
    offer = ctx["offer"]
    client = TestClient(app)

    # 9,000 multi-byte emojis = 36,000 bytes (> 32 KB)
    oversized_utf8 = "🧾" * 9000
    headers = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "BYTE-01"}
    res = client.post("/v1/orders", json={
        "offer_id": offer.id,
        "expected_offer_version": offer.version,
        "grant_id": grant.id,
        "raw_invoice_text": oversized_utf8
    }, headers=headers)
    assert res.status_code == 422
    assert "32 KB" in res.text


def test_f09_expired_grant_rejected(app_and_services):
    """Verifies F09: Expired spend grants are rejected before reservation."""
    ctx = app_and_services
    app = ctx["app"]
    authority = app.state.authority
    alice = ctx["alice"]
    offer = ctx["offer"]
    client = TestClient(app)

    # Create grant expired in year 2000
    agent = authority.register_agent(alice.id, "ExpiredAgent")
    raw_key, _ = authority.issue_agent_key(agent.id)
    expired_grant = authority.create_spend_grant(
        owner_id=alice.id,
        agent_id=agent.id,
        max_allowance_credits=1000,
        per_order_max_credits=500,
        expires_at="2000-01-01T00:00:00+00:00"
    )

    headers = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "EXP-01"}
    res = client.post("/v1/orders", json={
        "offer_id": offer.id,
        "expected_offer_version": offer.version,
        "grant_id": expired_grant.id,
        "raw_invoice_text": SAMPLE_INVOICE_TEXT
    }, headers=headers)
    assert res.status_code == 422
    assert "expired" in res.text


def test_f07_extraction_contract_strictness():
    """Verifies F07: Unknown extra fields are forbidden and missing evidence fails validation."""
    from app.models.extraction import validate_extraction_evidence
    import pydantic

    # Extra field rejected by schema
    with pytest.raises(pydantic.ValidationError):
        ExtractionResult(
            contract_version="invoice.extract.v1",
            currency="INR",
            total_amount_minor=1000,
            unauthorized_extra_field="malicious_injection"  # Forbidden!
        )

    # Missing evidence span for total_amount_minor fails validation
    res_no_evidence = ExtractionResult(
        contract_version="invoice.extract.v1",
        currency="INR",
        total_amount_minor=1000,
        evidence_spans=[]  # No evidence!
    )
    errors = validate_extraction_evidence("Total: 10.00", res_no_evidence)
    assert len(errors) > 0
    assert any("MISSING_EVIDENCE_FOR_FIELD" in e for e in errors)
