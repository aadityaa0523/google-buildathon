"""
Nexus SaaS Capability Marketplace: FastAPI Core Application
Provides authenticated REST API for Agentic Discovery, Purchasing, and Accountability.
Enforces role-based authority (F01) and public projection safety (F02).
"""

import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Header, Depends, Query, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.core.database import Database, global_db
from app.core.clock import Clock, global_clock
from app.core.seed import seed_demo_data
from app.models.authority import Owner, Agent
from app.models.offers import PublicOffer
from app.services.accounting_service import AccountingService
from app.services.authority_service import AuthorityService
from app.services.offer_service import OfferService
from app.services.fulfillment_service import FulfillmentService
from app.services.commerce_service import CommerceService
from app.services.accountability_service import AccountabilityService
from app.services.retention_service import RetentionService
from app.sellers.deterministic_seller import deterministic_seller_handler
from app.sellers.gemini_seller import gemini_seller_handler
from app.sellers.fault_seller import fault_seller_handler


def create_app(
    db: Optional[Database] = None,
    clock: Optional[Clock] = None,
    auto_seed: bool = False,
    enable_demo_mode: bool = True
) -> FastAPI:
    database = db or global_db
    app_clock = clock or global_clock

    # Wire up services
    accounting = AccountingService(database)
    authority = AuthorityService(database)
    offers = OfferService(database, allow_localhost_endpoints=True)
    fulfillment = FulfillmentService()
    commerce = CommerceService(database, accounting, authority, offers, fulfillment, clock=app_clock)
    accountability = AccountabilityService(database, accounting, clock=app_clock)
    retention = RetentionService(database, clock=app_clock)

    # Register demonstration sellers
    fulfillment.register_mock_seller("http://localhost:8000/sellers/deterministic", deterministic_seller_handler)
    fulfillment.register_mock_seller("http://localhost:8000/sellers/gemini", gemini_seller_handler)
    fulfillment.register_mock_seller("http://localhost:8000/sellers/fault", fault_seller_handler)

    if auto_seed:
        seed_demo_data(database, authority, offers, accounting)

    app = FastAPI(
        title="Nexus SaaS Marketplace",
        description="Agent-native SaaS capability marketplace with transparent terms, spend grants, and double-entry accounting.",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Store service references and mode in app state
    app.state.db = database
    app.state.clock = app_clock
    app.state.accounting = accounting
    app.state.authority = authority
    app.state.offers = offers
    app.state.fulfillment = fulfillment
    app.state.commerce = commerce
    app.state.accountability = accountability
    app.state.retention = retention
    app.state.enable_demo_mode = enable_demo_mode

    # --- AUTHENTICATION DEPENDENCIES (F01) ---
    def get_authenticated_agent(authorization: Optional[str] = Header(None)) -> tuple[Agent, Owner]:
        """Authenticates buyer agent bearer token."""
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or malformed Authorization header")
        token = authorization[len("Bearer "):].strip()
        try:
            agent, owner = authority.authenticate_agent_token(token)
            return agent, owner
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    def get_authenticated_owner(x_owner_id: Optional[str] = Header(None, alias="X-Owner-Id")) -> Owner:
        """Authenticates human owner role (F01)."""
        if not x_owner_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing X-Owner-Id authentication header")
        owner = authority.get_owner(x_owner_id)
        if not owner:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or unregistered owner identity")
        return owner

    def get_authenticated_operator(x_operator_key: Optional[str] = Header(None, alias="X-Operator-Key")) -> bool:
        """Authenticates marketplace operator role (F01)."""
        expected_key = os.environ.get("NEXUS_OPERATOR_KEY", "nexus_admin_operator_key_2026")
        if not x_operator_key or x_operator_key != expected_key:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Missing or invalid operator credentials")
        return True

    web_dir = os.path.join(os.path.dirname(__file__), "web")
    index_path = os.path.join(web_dir, "index.html")

    # --- PUBLIC & CONSOLE ROUTES ---
    @app.get("/console", response_class=FileResponse)
    def serve_console():
        if os.path.exists(index_path):
            return FileResponse(index_path, media_type="text/html")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Console interface not found")

    @app.get("/")
    def health_check(request: Request):
        accept = request.headers.get("accept", "")
        if "text/html" in accept and os.path.exists(index_path):
            return FileResponse(index_path, media_type="text/html")
        return {
            "service": "Nexus SaaS Capability Marketplace",
            "status": "OPERATIONAL",
            "time": app_clock.now_iso(),
            "contract": "invoice.extract.v1",
            "console_url": "/console"
        }

    @app.get("/v1/demo_actor")
    def get_demo_actor():
        """Returns ready-to-use demo credentials in authorized demo mode (F01)."""
        if not app.state.enable_demo_mode:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Demo actor generation disabled in non-demo environment")
        return seed_demo_data(database, authority, offers, accounting)

    schemas_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "schemas")
    agent_card_path = os.path.join(schemas_dir, "a2a-agent-card.json")

    @app.get("/.well-known/agent.json")
    @app.get("/v1/agent-card")
    def get_agent_card():
        """Returns A2A standard Agent Card for automated protocol discovery."""
        if os.path.exists(agent_card_path):
            with open(agent_card_path, "r", encoding="utf-8") as f:
                import json
                return json.load(f)
        raise HTTPException(status_code=404, detail="Agent Card not found")

    @app.get("/v1/offers")
    def search_offers(
        capability_id: str = "invoice.extract.v1",
        max_buyer_price: Optional[int] = Query(None, description="Max test-credit price ceiling"),
        sort_by: str = Query("price_asc", enum=["price_asc", "rating_desc", "latency_asc"])
    ) -> List[PublicOffer]:
        """Discover and compare competing SaaS capability offers without leaking secrets (F02)."""
        return offers.search_offers(capability_id=capability_id, max_buyer_price=max_buyer_price, sort_by=sort_by)

    @app.get("/v1/offers/{offer_id}")
    def get_offer(offer_id: str) -> PublicOffer:
        """Retrieve public offer details, strictly omitting seller secrets (F02)."""
        offer = offers.get_public_offer(offer_id)
        if not offer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found")
        return offer

    @app.get("/v1/sellers/{seller_id}")
    def get_seller_profile(seller_id: str):
        with database.transaction() as conn:
            seller = conn.execute("SELECT * FROM sellers WHERE id = ?", (seller_id,)).fetchone()
            if not seller:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")
            reviews = conn.execute("SELECT * FROM reviews WHERE seller_id = ? AND is_common_owner = 0", (seller_id,)).fetchall()
            return {
                "seller": dict(seller),
                "reviews": [dict(r) for r in reviews]
            }

    # --- OWNER / ONBOARDING ROUTES (SECURED VIA F01) ---
    class CreateOwnerRequest(BaseModel):
        email: str
        name: str

    @app.post("/v1/owners")
    def create_owner(req: CreateOwnerRequest):
        return authority.create_owner(req.email, req.name)

    class RegisterAgentRequest(BaseModel):
        owner_id: str
        name: str

    @app.post("/v1/agents")
    def register_agent(req: RegisterAgentRequest, owner: Owner = Depends(get_authenticated_owner)):
        if req.owner_id != owner.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot register agent for another owner")
        return authority.register_agent(req.owner_id, req.name)

    @app.post("/v1/agents/{agent_id}/keys")
    def issue_agent_key(agent_id: str, owner: Owner = Depends(get_authenticated_owner)):
        with database.transaction() as conn:
            agent_row = conn.execute("SELECT owner_id FROM agents WHERE id = ?", (agent_id,)).fetchone()
            if not agent_row:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
            if agent_row["owner_id"] != owner.id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized: Agent belongs to another owner")
        raw_key, cred = authority.issue_agent_key(agent_id)
        return {
            "api_key": raw_key,
            "credential_id": cred.id,
            "key_prefix": cred.key_prefix,
            "warning": "Copy this token now; it cannot be viewed again."
        }

    class CreateGrantRequest(BaseModel):
        owner_id: str
        agent_id: str
        max_allowance_credits: int
        per_order_max_credits: int
        allowed_capabilities: Optional[List[str]] = None
        expires_at: Optional[str] = None

    @app.post("/v1/spend_grants")
    def create_spend_grant(req: CreateGrantRequest, owner: Owner = Depends(get_authenticated_owner)):
        if req.owner_id != owner.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot create spend grant for another owner")
        return authority.create_spend_grant(
            owner_id=req.owner_id,
            agent_id=req.agent_id,
            max_allowance_credits=req.max_allowance_credits,
            per_order_max_credits=req.per_order_max_credits,
            allowed_capabilities=req.allowed_capabilities,
            expires_at=req.expires_at
        )

    @app.post("/v1/accounts/{owner_id}/seed")
    def seed_wallet_balance(
        owner_id: str,
        amount_credits: int = Query(..., ge=1),
        _op: bool = Depends(get_authenticated_operator)
    ):
        new_balance = accounting.seed_wallet(owner_id, amount_credits)
        return {"owner_id": owner_id, "available_credits": new_balance}

    @app.get("/v1/accounts/{owner_id}")
    def get_account_balance(owner_id: str):
        return accounting.get_or_create_account(owner_id, "BUYER")

    # --- BUYER AGENT COMMERCE ROUTES ---
    class PurchaseOrderRequest(BaseModel):
        offer_id: str
        expected_offer_version: int = 1
        grant_id: str
        raw_invoice_text: str = Field(..., min_length=10, max_length=10000)

    @app.post("/v1/orders")
    def purchase_capability(
        req: PurchaseOrderRequest,
        idempotency_key: str = Header(..., alias="Idempotency-Key"),
        auth: tuple = Depends(get_authenticated_agent)
    ):
        agent, owner = auth
        try:
            order = commerce.purchase(
                agent=agent,
                owner=owner,
                offer_id=req.offer_id,
                expected_offer_version=req.expected_offer_version,
                grant_id=req.grant_id,
                raw_invoice_text=req.raw_invoice_text,
                idempotency_key=idempotency_key
            )
            return order
        except ValueError as e:
            msg = str(e)
            if "IDEMPOTENCY_CONFLICT" in msg:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
            if "OFFER_CHANGED" in msg:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
            if "POLICY_DENIAL" in msg or "INSUFFICIENT" in msg or "INVALID_INPUT" in msg:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=msg)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

    @app.get("/v1/orders/{order_id}")
    def get_order_details(order_id: str, auth: tuple = Depends(get_authenticated_agent)):
        agent, owner = auth
        order = commerce.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        if order.buyer_owner_id != owner.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized order access")
        return order

    @app.get("/v1/orders/{order_id}/result")
    def get_order_result(order_id: str, auth: tuple = Depends(get_authenticated_agent)):
        agent, owner = auth
        order = commerce.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        if order.buyer_owner_id != owner.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized order access")
        if not order.result_payload_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order has no completed result payload")
        try:
            content = commerce.get_order_payload(order.result_payload_id, owner.id)
            import json
            return json.loads(content)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_410_GONE, detail=str(e))

    @app.post("/v1/orders/{order_id}/cancel")
    def cancel_order(order_id: str, auth: tuple = Depends(get_authenticated_agent)):
        agent, owner = auth
        try:
            return commerce.cancel_order(order_id, owner.id)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # --- REVIEWS & DISPUTES ---
    class SubmitReviewRequest(BaseModel):
        order_id: str
        rating: int = Field(..., ge=1, le=5)
        comment: str = Field(..., max_length=1000)

    @app.post("/v1/reviews")
    def submit_review(req: SubmitReviewRequest, auth: tuple = Depends(get_authenticated_agent)):
        agent, owner = auth
        try:
            return accountability.submit_review(req.order_id, owner.id, req.rating, req.comment)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    class OpenDisputeRequest(BaseModel):
        order_id: str
        reason: str
        details: str

    @app.post("/v1/disputes")
    def open_dispute(req: OpenDisputeRequest, auth: tuple = Depends(get_authenticated_agent)):
        agent, owner = auth
        try:
            return accountability.open_dispute(req.order_id, owner.id, req.reason, req.details)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # --- OPERATOR ADJUDICATION & CLEANUP (SECURED VIA F01) ---
    class AdjudicateRequest(BaseModel):
        approved: bool
        operator_reason: str

    @app.post("/v1/operator/disputes/{dispute_id}/adjudicate")
    def adjudicate_dispute(
        dispute_id: str,
        req: AdjudicateRequest,
        _op: bool = Depends(get_authenticated_operator)
    ):
        try:
            return accountability.adjudicate_dispute(dispute_id, req.approved, req.operator_reason)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @app.post("/v1/operator/retention/sweep")
    def run_retention_sweep(_op: bool = Depends(get_authenticated_operator)):
        purged = retention.sweep_expired_payloads()
        return {"purged_payloads_count": purged, "status": "COMPLETED"}

    return app


app = create_app(auto_seed=True)
