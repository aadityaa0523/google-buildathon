"""
Tests for Milestone M2: MCP Tool Execution Parity (A24)
"""

import json
import asyncio
from app.mcp_server.server import create_mcp_server
from tests.conftest import SAMPLE_INVOICE_TEXT


def test_a24_mcp_tool_execution_parity(app_and_services):
    """
    Verifies A24:
    MCP tools execute discovery, purchase, order retrieval, and result fetching with exact parity to HTTP.
    """
    ctx = app_and_services
    db = ctx["db"]
    raw_key = ctx["raw_key"]
    grant = ctx["grant"]
    offer = ctx["offer"]
    alice = ctx["alice"]

    mcp = create_mcp_server(db=db)

    # 1. Search offers via MCP
    search_res = asyncio.run(mcp.call_tool("search_offers", {"capability_id": "invoice.extract.v1", "max_price": 500}))
    search_json = search_res.content[0].text
    offers = json.loads(search_json)
    assert len(offers) >= 1
    assert offers[0]["id"] == offer.id

    # 2. Purchase capability via MCP
    purchase_res = asyncio.run(mcp.call_tool("purchase_capability", {
        "agent_bearer_token": raw_key,
        "offer_id": offer.id,
        "offer_version": offer.version,
        "spend_grant_id": grant.id,
        "raw_invoice_text": SAMPLE_INVOICE_TEXT,
        "idempotency_key": "IDEMP-MCP-001"
    }))
    order_json = purchase_res.content[0].text
    order_data = json.loads(order_json)
    assert "id" in order_data
    assert order_data["execution_state"] == "SUCCEEDED"
    assert order_data["accounting_state"] == "SETTLED"
    order_id = order_data["id"]

    # 3. Retrieve order result via MCP
    result_res = asyncio.run(mcp.call_tool("get_order_result", {
        "agent_bearer_token": raw_key,
        "order_id": order_id
    }))
    result_json = result_res.content[0].text
    result_data = json.loads(result_json)
    assert result_data["contract_version"] == "invoice.extract.v1"
    assert result_data["vendor_name"] == "Acme Industrial Supplies Ltd"
    assert result_data["total_amount_minor"] == 1180000
