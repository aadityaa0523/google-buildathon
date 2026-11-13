"""
Tests for Milestone M3: Accountability, Reviews, Disputes, and Retention Expiry (A18..A22)
"""

from starlette.testclient import TestClient
from tests.conftest import SAMPLE_INVOICE_TEXT


def test_a18_reviews_and_self_dealing_exclusion(app_and_services):
    """
    Verifies A18:
    - Order-backed reviews can be submitted.
    - If buyer and seller share the same owner, the review is marked is_common_owner=True
      and excluded from the seller's public average score.
    """
    ctx = app_and_services
    app = ctx["app"]
    raw_key = ctx["raw_key"]
    grant = ctx["grant"]
    offer = ctx["offer"]
    bob = ctx["bob"]

    client = TestClient(app)

    # 1. Purchase an order as Alice
    headers = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "IDEMP-REV-01"}
    resp = client.post("/v1/orders", json={
        "offer_id": offer.id,
        "expected_offer_version": offer.version,
        "grant_id": grant.id,
        "raw_invoice_text": SAMPLE_INVOICE_TEXT
    }, headers=headers)
    order_id = resp.json()["id"]

    # 2. Alice submits a 5-star review (Independent trade)
    rev_resp = client.post("/v1/reviews", json={
        "order_id": order_id,
        "rating": 5,
        "comment": "Fast and flawless evidence extraction!"
    }, headers=headers)
    assert rev_resp.status_code == 200
    rev_data = rev_resp.json()
    assert rev_data["is_common_owner"] is False

    # Seller average rating should be 5.0
    offer_after = app.state.offers.get_offer(offer.id)
    assert offer_after.average_rating == 5.0
    assert offer_after.rating_count == 1

    # 3. Now Bob (seller owner) creates an agent for himself and reviews himself (Self-dealing)
    bob_agent = app.state.authority.register_agent(bob.id, "BobSelfAgent")
    bob_key, _ = app.state.authority.issue_agent_key(bob_agent.id)
    app.state.accounting.seed_wallet(bob.id, 1000)
    bob_grant = app.state.authority.create_spend_grant(bob.id, bob_agent.id, 500, 200)

    bob_headers = {"Authorization": f"Bearer {bob_key}", "Idempotency-Key": "IDEMP-SELF-01"}
    resp_self = client.post("/v1/orders", json={
        "offer_id": offer.id,
        "expected_offer_version": offer.version,
        "grant_id": bob_grant.id,
        "raw_invoice_text": SAMPLE_INVOICE_TEXT
    }, headers=bob_headers)
    order_self_id = resp_self.json()["id"]

    # Bob submits a 5-star review on his own seller
    rev_self_resp = client.post("/v1/reviews", json={
        "order_id": order_self_id,
        "rating": 5,
        "comment": "I am the best seller ever!"
    }, headers=bob_headers)
    assert rev_self_resp.status_code == 200
    assert rev_self_resp.json()["is_common_owner"] is True

    # Rating count for public score should still be 1, because self-dealing review was excluded!
    offer_self_check = app.state.offers.get_offer(offer.id)
    assert offer_self_check.rating_count == 1


def test_a19_dispute_human_adjudication_and_refund(app_and_services):
    """
    Verifies A19:
    Buyer opens a dispute within 24h -> Human operator adjudicates and approves ->
    Seller net and platform fee are reversed, buyer credits are fully restored.
    """
    ctx = app_and_services
    app = ctx["app"]
    raw_key = ctx["raw_key"]
    grant = ctx["grant"]
    offer = ctx["offer"]
    alice = ctx["alice"]
    seller = ctx["seller"]

    client = TestClient(app)

    # 1. Complete order
    headers = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "IDEMP-DISP-01"}
    resp = client.post("/v1/orders", json={
        "offer_id": offer.id,
        "expected_offer_version": offer.version,
        "grant_id": grant.id,
        "raw_invoice_text": SAMPLE_INVOICE_TEXT
    }, headers=headers)
    order_id = resp.json()["id"]

    # Buyer wallet is now 4900
    buyer_bal = ctx["db"].get_connection().execute("SELECT available_credits FROM accounts WHERE account_id = ?", (alice.id,)).fetchone()
    assert buyer_bal["available_credits"] == 4900

    # 2. Buyer opens dispute
    disp_resp = client.post("/v1/disputes", json={
        "order_id": order_id,
        "reason": "SEMANTIC_TOTAL_ERROR",
        "details": "The vendor total was extracted incorrectly from the footer."
    }, headers=headers)
    assert disp_resp.status_code == 200
    dispute_id = disp_resp.json()["id"]

    # 3. Operator reviews evidence and approves refund (POST /v1/operator/disputes/{id}/adjudicate)
    adj_resp = client.post(
        f"/v1/operator/disputes/{dispute_id}/adjudicate",
        json={
            "approved": True,
            "operator_reason": "Verified contract breach: total missed last digit."
        },
        headers={"X-Operator-Key": "nexus_admin_operator_key_2026"}
    )
    assert adj_resp.status_code == 200
    assert adj_resp.json()["status"] == "RESOLVED_REFUNDED"

    # 4. Verify Accounting Reversal
    # Buyer: 4900 + 100 = 5000 restored!
    buyer_restored = ctx["db"].get_connection().execute("SELECT available_credits FROM accounts WHERE account_id = ?", (alice.id,)).fetchone()
    assert buyer_restored["available_credits"] == 5000

    # Seller: 85 - 85 = 0
    seller_restored = ctx["db"].get_connection().execute("SELECT available_credits FROM accounts WHERE account_id = ?", (seller.id,)).fetchone()
    assert seller_restored["available_credits"] == 0

    # Grant: spent credits restored from 100 back to 0!
    grant_restored = app.state.authority.get_spend_grant(grant.id)
    assert grant_restored.spent_credits == 0


def test_a21_a22_retention_expiry_and_active_deletion(app_and_services):
    """
    Verifies A21 & A22:
    - 24h after completion, payload access is denied immediately via application check (410 Gone).
    - Deletion sweeper permanently purges raw content text.
    """
    ctx = app_and_services
    app = ctx["app"]
    raw_key = ctx["raw_key"]
    grant = ctx["grant"]
    offer = ctx["offer"]
    clock = ctx["clock"]

    client = TestClient(app)

    headers = {"Authorization": f"Bearer {raw_key}", "Idempotency-Key": "IDEMP-RET-01"}
    resp = client.post("/v1/orders", json={
        "offer_id": offer.id,
        "expected_offer_version": offer.version,
        "grant_id": grant.id,
        "raw_invoice_text": SAMPLE_INVOICE_TEXT
    }, headers=headers)
    order_id = resp.json()["id"]

    # Payload is retrievable within 24h
    res1 = client.get(f"/v1/orders/{order_id}/result", headers=headers)
    assert res1.status_code == 200

    # Advance clock by 25 hours (Past the 24-hour retention window)
    clock.advance(hours=25)

    # Attempt to read result -> Denied with 410 GONE! (A21)
    res2 = client.get(f"/v1/orders/{order_id}/result", headers=headers)
    assert res2.status_code == 410
    assert "PAYLOAD_ACCESS_EXPIRED" in res2.text

    # Run active deletion sweeper (A21)
    sweep_resp = client.post("/v1/operator/retention/sweep", headers={"X-Operator-Key": "nexus_admin_operator_key_2026"})
    assert sweep_resp.status_code == 200
    assert sweep_resp.json()["purged_payloads_count"] >= 1
