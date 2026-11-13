"""
Tests for Milestone M2: Enforce Authority, Concurrency, and Failure Invariants (A02..A14)
"""

from starlette.testclient import TestClient
from app.sellers.fault_seller import set_fault_mode, FAULT_MODE_TIMEOUT, FAULT_MODE_SCHEMA_ERROR, FAULT_MODE_NONE
from tests.conftest import SAMPLE_INVOICE_TEXT


def test_a04_idempotency_replay_and_conflict(app_and_services):
    """
    Verifies A04:
    - Replaying exact same request returns identical order without extra charges.
    - Reusing key with different body raises IDEMPOTENCY_CONFLICT (HTTP 409).
    """
    ctx = app_and_services
    app = ctx["app"]
    raw_key = ctx["raw_key"]
    grant = ctx["grant"]
    offer = ctx["offer"]

    client = TestClient(app)
    headers = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "IDEMP-KEY-999"}
    payload = {
        "offer_id": offer.id,
        "expected_offer_version": offer.version,
        "grant_id": grant.id,
        "raw_invoice_text": SAMPLE_INVOICE_TEXT
    }

    # 1. First purchase
    resp1 = client.post("/v1/orders", json=payload, headers=headers)
    assert resp1.status_code == 200
    order1 = resp1.json()

    # 2. Replay with identical payload -> must return same order
    resp2 = client.post("/v1/orders", json=payload, headers=headers)
    assert resp2.status_code == 200
    order2 = resp2.json()
    assert order1["id"] == order2["id"]

    # 3. Replay with changed body -> must return 409 Conflict
    payload_changed = dict(payload, raw_invoice_text=SAMPLE_INVOICE_TEXT + "\nExtra modified line")
    resp3 = client.post("/v1/orders", json=payload_changed, headers=headers)
    assert resp3.status_code == 409
    assert "IDEMPOTENCY_CONFLICT" in resp3.text


def test_a02_grant_budget_ceiling_enforcement(app_and_services):
    """
    Verifies A02:
    Purchases exceeding spend grant headroom or per-order cap are deterministically rejected.
    """
    ctx = app_and_services
    app = ctx["app"]
    raw_key = ctx["raw_key"]
    grant = ctx["grant"]
    seller = ctx["seller"]

    # Publish an expensive offer that exceeds Alice's per-order cap (250 credits)
    expensive_offer = app.state.offers.publish_offer(
        seller_id=seller.id,
        title="Expensive Enterprise Extractor",
        description="High volume document batch",
        buyer_total_credits=500,
        seller_net_credits=425,
        nexus_fee_credits=75,
        endpoint_url="http://localhost:8000/sellers/deterministic"
    )

    client = TestClient(app)
    headers = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "IDEMP-EXPENSIVE-001"}
    payload = {
        "offer_id": expensive_offer.id,
        "expected_offer_version": 1,
        "grant_id": grant.id,
        "raw_invoice_text": SAMPLE_INVOICE_TEXT
    }
    resp = client.post("/v1/orders", json=payload, headers=headers)
    assert resp.status_code == 422
    assert "AMOUNT_EXCEEDS_PER_ORDER_CAP" in resp.text


def test_a05_stale_offer_version_rejection(app_and_services):
    """
    Verifies A05:
    If a buyer attempts to purchase with an outdated offer version, reject with 409 OFFER_CHANGED.
    """
    ctx = app_and_services
    app = ctx["app"]
    raw_key = ctx["raw_key"]
    grant = ctx["grant"]
    offer = ctx["offer"]

    client = TestClient(app)
    headers = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "IDEMP-STALE-001"}
    payload = {
        "offer_id": offer.id,
        "expected_offer_version": 999,  # Stale version!
        "grant_id": grant.id,
        "raw_invoice_text": SAMPLE_INVOICE_TEXT
    }
    resp = client.post("/v1/orders", json=payload, headers=headers)
    assert resp.status_code == 409
    assert "OFFER_CHANGED" in resp.text


def test_a09_seller_timeout_releases_reserved_credits(app_and_services):
    """
    Verifies A09 & A12:
    When seller times out or fails, reserved credits are safely returned to buyer wallet and grant.
    """
    ctx = app_and_services
    app = ctx["app"]
    raw_key = ctx["raw_key"]
    grant = ctx["grant"]
    seller = ctx["seller"]
    alice = ctx["alice"]

    fault_offer = app.state.offers.publish_offer(
        seller_id=seller.id,
        title="Faulty Seller",
        description="Simulates timeout",
        buyer_total_credits=100,
        seller_net_credits=85,
        nexus_fee_credits=15,
        endpoint_url="http://localhost:8000/sellers/fault"
    )

    set_fault_mode(FAULT_MODE_TIMEOUT)
    try:
        client = TestClient(app)
        headers = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "IDEMP-TIMEOUT-001"}
        payload = {
            "offer_id": fault_offer.id,
            "expected_offer_version": 1,
            "grant_id": grant.id,
            "raw_invoice_text": SAMPLE_INVOICE_TEXT
        }
        resp = client.post("/v1/orders", json=payload, headers=headers)
        assert resp.status_code == 200
        order_data = resp.json()
        assert order_data["execution_state"] in ("FAILED", "EXPIRED")
        assert order_data["accounting_state"] == "RELEASED"

        # Check that buyer wallet was completely released back to 5000
        buyer_bal = ctx["db"].get_connection().execute("SELECT available_credits, reserved_credits FROM accounts WHERE account_id = ?", (alice.id,)).fetchone()
        assert buyer_bal["available_credits"] == 5000
        assert buyer_bal["reserved_credits"] == 0

        # Grant was also released
        grant_after = app.state.authority.get_spend_grant(grant.id)
        assert grant_after.spent_credits == 0
        assert grant_after.reserved_credits == 0
    finally:
        set_fault_mode(FAULT_MODE_NONE)
