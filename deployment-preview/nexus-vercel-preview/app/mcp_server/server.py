"""
Nexus MCP (Model Context Protocol) Server
Exposes discovery, purchasing, and order management tools directly to autonomous LLM agents.
Compatible with MCP SDK 2.x.
"""

import json
from typing import Any, Dict, List, Optional
from mcp.server.mcpserver import MCPServer

from app.core.database import global_db
from app.services.accounting_service import AccountingService
from app.services.authority_service import AuthorityService
from app.services.offer_service import OfferService
from app.services.fulfillment_service import FulfillmentService
from app.services.commerce_service import CommerceService
from app.services.accountability_service import AccountabilityService


def create_mcp_server(db=None) -> MCPServer:
    database = db or global_db
    accounting = AccountingService(database)
    authority = AuthorityService(database)
    offers = OfferService(database, allow_localhost_endpoints=True)
    fulfillment = FulfillmentService()
    from app.sellers.deterministic_seller import deterministic_seller_handler
    from app.sellers.gemini_seller import gemini_seller_handler
    from app.sellers.fault_seller import fault_seller_handler

    fulfillment.register_mock_seller("http://localhost:8000/sellers/deterministic", deterministic_seller_handler)
    fulfillment.register_mock_seller("http://localhost:8000/sellers/gemini", gemini_seller_handler)
    fulfillment.register_mock_seller("http://localhost:8000/sellers/fault", fault_seller_handler)

    commerce = CommerceService(database, accounting, authority, offers, fulfillment)
    accountability = AccountabilityService(database, accounting)

    mcp = MCPServer("Nexus Marketplace")

    @mcp.tool()
    def search_offers(capability_id: str = "invoice.extract.v1", max_price: Optional[int] = None) -> str:
        """
        Discover and compare competing SaaS capability offers on Nexus.
        Returns list of transparent offers with full buyer charge, fee, and seller net in test credits.
        """
        results = offers.search_offers(capability_id=capability_id, max_buyer_price=max_price)
        return json.dumps([o.model_dump() for o in results], indent=2)

    @mcp.tool()
    def get_offer_details(offer_id: str) -> str:
        """Get public terms, deadline policy, and historical quality metrics for a specific offer (F02 safe)."""
        pub_offer = offers.get_public_offer(offer_id)
        if not pub_offer:
            return json.dumps({"error": "Offer not found"})
        return json.dumps(pub_offer.model_dump(), indent=2)

    @mcp.tool()
    def purchase_capability(
        agent_bearer_token: str,
        offer_id: str,
        offer_version: int,
        spend_grant_id: str,
        raw_invoice_text: str,
        idempotency_key: str
    ) -> str:
        """
        Purchase capability execution under owner-authorized spend grant limits.
        Atomically reserves test credits and dispatches to chosen seller.
        """
        try:
            agent, owner = authority.authenticate_agent_token(agent_bearer_token)
            order = commerce.purchase(
                agent=agent,
                owner=owner,
                offer_id=offer_id,
                expected_offer_version=offer_version,
                grant_id=spend_grant_id,
                raw_invoice_text=raw_invoice_text,
                idempotency_key=idempotency_key
            )
            return json.dumps(order.model_dump(), indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    def get_order_status(agent_bearer_token: str, order_id: str) -> str:
        """Retrieve execution and accounting status of an order."""
        try:
            agent, owner = authority.authenticate_agent_token(agent_bearer_token)
            order = commerce.get_order_by_id(order_id)
            if not order:
                return json.dumps({"error": "Order not found"})
            if order.buyer_owner_id != owner.id:
                return json.dumps({"error": "Unauthorized order access"})
            return json.dumps(order.model_dump(), indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    def get_order_result(agent_bearer_token: str, order_id: str) -> str:
        """Fetch validated extracted JSON payload for a succeeded order (enforces 24h retention window)."""
        try:
            agent, owner = authority.authenticate_agent_token(agent_bearer_token)
            order = commerce.get_order_by_id(order_id)
            if not order or not order.result_payload_id:
                return json.dumps({"error": "Result not available"})
            if order.buyer_owner_id != owner.id:
                return json.dumps({"error": "Unauthorized order access"})
            content = commerce.get_order_payload(order.result_payload_id, owner.id)
            return content
        except Exception as e:
            return json.dumps({"error": str(e)})

    return mcp
