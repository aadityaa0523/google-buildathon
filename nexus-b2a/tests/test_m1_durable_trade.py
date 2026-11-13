"""
Tests for Milestone M1: First Complete Durable Trade (A01)
"""

from starlette.testclient import TestClient
from tests.conftest import SAMPLE_INVOICE_TEXT


def test_m1_complete_durable_trade_happy_path(app_and_services):
    """
    Verifies A01:
    Discover offer -> Purchase with locked terms -> Settle test credits -> Fetch result and receipt.
    """
    ctx = app_and_services
    app = ctx["app"]
    raw_key = ctx["raw_key"]
    grant = ctx["grant"]
    offer = ctx["offer"]
    alice = ctx["alice"]
    seller = ctx["seller"]

    client = TestClient(app)

    # 1. Discover offers (Public API)
    resp = client.get("/v1/offers")
    assert resp.status_code == 200
    offers_list = resp.json()
    assert len(offers_list) >= 1
    found_offer = offers_list[0]
    assert found_offer["id"] == offer.id
    assert found_offer["pricing"]["buyer_total_credits"] == 100
    assert found_offer["pricing"]["seller_net_credits"] == 85
    assert found_offer["pricing"]["nexus_fee_credits"] == 15

    # 2. Check initial balances
    buyer_bal = ctx["db"].get_connection().execute("SELECT available_credits, reserved_credits FROM accounts WHERE account_id = ?", (alice.id,)).fetchone()
    assert buyer_bal["available_credits"] == 5000
    assert buyer_bal["reserved_credits"] == 0

    # 3. Buyer Agent Purchases Capability (POST /v1/orders)
    headers = {
        "Authorization": f"Bearer {raw_key}",
        "Idempotency-Key": "IDEMP-TRADE-001"
    }
    order_payload = {
        "offer_id": offer.id,
        "expected_offer_version": offer.version,
        "grant_id": grant.id,
        "raw_invoice_text": SAMPLE_INVOICE_TEXT
    }
    purchase_resp = client.post("/v1/orders", json=order_payload, headers=headers)
    assert purchase_resp.status_code == 200, f"Purchase failed: {purchase_resp.text}"
    order_data = purchase_resp.json()
    
    order_id = order_data["id"]
    assert order_data["execution_state"] == "SUCCEEDED"
    assert order_data["accounting_state"] == "SETTLED"
    assert order_data["pricing"]["buyer_total_credits"] == 100

    # 4. Verify Financial Settlement (Double-Entry Balance Preservation)
    # Buyer: 5000 - 100 = 4900 available, 0 reserved
    buyer_bal_after = ctx["db"].get_connection().execute("SELECT available_credits, reserved_credits FROM accounts WHERE account_id = ?", (alice.id,)).fetchone()
    assert buyer_bal_after["available_credits"] == 4900
    assert buyer_bal_after["reserved_credits"] == 0

    # Seller: 0 + 85 = 85 available
    seller_bal = ctx["db"].get_connection().execute("SELECT available_credits FROM accounts WHERE account_id = ?", (seller.id,)).fetchone()
    assert seller_bal["available_credits"] == 85

    # Platform fees: 0 + 15 = 15 available
    fee_bal = ctx["db"].get_connection().execute("SELECT available_credits FROM accounts WHERE account_id = 'platform_fees'").fetchone()
    assert fee_bal["available_credits"] == 15

    # Spend grant: 100 spent, 0 reserved
    grant_after = ctx["app"].state.authority.get_spend_grant(grant.id)
    assert grant_after.spent_credits == 100
    assert grant_after.reserved_credits == 0
    assert grant_after.available_credits == 900

    # 5. Fetch Extracted Result (GET /v1/orders/{order_id}/result)
    result_resp = client.get(f"/v1/orders/{order_id}/result", headers=headers)
    assert result_resp.status_code == 200
    result_data = result_resp.json()
    assert result_data["contract_version"] == "invoice.extract.v1"
    assert result_data["vendor_name"] == "Acme Industrial Supplies Ltd"
    assert result_data["total_amount_minor"] == 1180000
    assert len(result_data["evidence_spans"]) >= 3
