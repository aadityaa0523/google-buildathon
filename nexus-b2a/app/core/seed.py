"""
Nexus Demo Seed Data Initializer
Populates demonstration sellers, offers, test wallets, and default buyer agents.
"""

from typing import Dict, Any
from app.core.database import Database
from app.services.authority_service import AuthorityService
from app.services.offer_service import OfferService
from app.services.accounting_service import AccountingService


def seed_demo_data(
    db: Database,
    authority: AuthorityService,
    offers: OfferService,
    accounting: AccountingService
) -> Dict[str, Any]:
    """
    Seeds initial demo sellers, offers, buyer owner, and test credentials if empty.
    Returns a dictionary of the seeded actors and resources.
    """
    with db.transaction() as conn:
        existing_offers = conn.execute("SELECT COUNT(*) as count FROM offers").fetchone()["count"]

    if existing_offers > 0:
        # Already seeded, fetch existing
        with db.transaction() as conn:
            buyer_owner = conn.execute("SELECT * FROM owners WHERE email = 'console.operator@nexus.local'").fetchone()
            if buyer_owner:
                agent = conn.execute("SELECT * FROM agents WHERE owner_id = ?", (buyer_owner["id"],)).fetchone()
                grant = conn.execute("SELECT * FROM spend_grants WHERE owner_id = ?", (buyer_owner["id"],)).fetchone()
                all_offers = conn.execute("SELECT id, title, buyer_total_credits FROM offers").fetchall()
                raw_key, _ = authority.issue_agent_key(agent["id"]) if agent else ("none", None)
                return {
                    "buyer_owner_id": buyer_owner["id"],
                    "buyer_agent_id": agent["id"] if agent else None,
                    "buyer_agent_key": raw_key,
                    "grant_id": grant["id"] if grant else None,
                    "offers": [dict(o) for o in all_offers]
                }

    # 1. Seed Seller 1: DocuExtract Pro (Deterministic RegEx & Rule-based)
    owner_1 = authority.create_owner("sales@docuextract.ai", "DocuExtract Inc")
    seller_1 = offers.register_seller(owner_1.id, "DocuExtract Pro")
    offer_1 = offers.publish_offer(
        seller_id=seller_1.id,
        title="DocuExtract Ultra (Deterministic)",
        description="Ultra-fast deterministic rule-based invoice extraction with strict evidence spans.",
        buyer_total_credits=50,
        seller_net_credits=45,
        nexus_fee_credits=5,
        execution_deadline_seconds=10,
        endpoint_url="http://localhost:8000/sellers/deterministic",
        endpoint_secret="docu_secret_key_8841"
    )

    # 2. Seed Seller 2: Gemini 2.5 Flash Vision & Text Intelligence
    owner_2 = authority.create_owner("gemini.sales@google.cloud", "Google Cloud AI Solutions")
    seller_2 = offers.register_seller(owner_2.id, "Gemini Flash OCR & Extractor")
    offer_2 = offers.publish_offer(
        seller_id=seller_2.id,
        title="Gemini 2.5 Flash Multimodal Extractor",
        description="State-of-the-art multimodal AI extraction using Gemini 2.5 Flash with character offset validation.",
        buyer_total_credits=100,
        seller_net_credits=90,
        nexus_fee_credits=10,
        execution_deadline_seconds=15,
        endpoint_url="http://localhost:8000/sellers/gemini",
        endpoint_secret="gemini_secret_key_2026"
    )

    # 3. Seed Seller 3: Fault Injector Test Service (demonstrating timeout, bad evidence, refund)
    owner_3 = authority.create_owner("chaos@faultylabs.dev", "Chaos Engineering Labs")
    seller_3 = offers.register_seller(owner_3.id, "Faulty Edge Test")
    offer_3 = offers.publish_offer(
        seller_id=seller_3.id,
        title="Fault Injector (Timeout & Bad Evidence Demo)",
        description="Demonstration seller testing edge cases: SLA timeouts, schema non-conformance, and automated refund triggers.",
        buyer_total_credits=30,
        seller_net_credits=27,
        nexus_fee_credits=3,
        execution_deadline_seconds=5,
        endpoint_url="http://localhost:8000/sellers/fault",
        endpoint_secret="fault_secret_key_9999"
    )

    # 4. Seed Buyer Owner & Test Wallet
    buyer_owner = authority.create_owner("console.operator@nexus.local", "Console Operator")
    accounting.seed_wallet(buyer_owner.id, 10000)

    # 5. Seed Buyer Agent
    buyer_agent = authority.register_agent(buyer_owner.id, "WebTesterAgent")
    raw_key, cred = authority.issue_agent_key(buyer_agent.id)

    # 6. Seed Spend Grant
    grant = authority.create_spend_grant(
        owner_id=buyer_owner.id,
        agent_id=buyer_agent.id,
        max_allowance_credits=5000,
        per_order_max_credits=500,
        allowed_capabilities=["invoice.extract.v1"]
    )

    # Update seller metrics for realistic display
    with db.transaction() as conn:
        conn.execute("UPDATE offers SET p95_latency_ms = 120, success_rate_pct = 99.8, average_rating = 4.9, rating_count = 128 WHERE id = ?", (offer_1.id,))
        conn.execute("UPDATE offers SET p95_latency_ms = 820, success_rate_pct = 98.9, average_rating = 4.8, rating_count = 85 WHERE id = ?", (offer_2.id,))
        conn.execute("UPDATE offers SET p95_latency_ms = 4200, success_rate_pct = 62.0, average_rating = 2.3, rating_count = 14 WHERE id = ?", (offer_3.id,))

    return {
        "buyer_owner_id": buyer_owner.id,
        "buyer_agent_id": buyer_agent.id,
        "buyer_agent_key": raw_key,
        "grant_id": grant.id,
        "offers": [
            {"id": offer_1.id, "title": offer_1.title, "buyer_total_credits": 50},
            {"id": offer_2.id, "title": offer_2.title, "buyer_total_credits": 100},
            {"id": offer_3.id, "title": offer_3.title, "buyer_total_credits": 30}
        ]
    }
