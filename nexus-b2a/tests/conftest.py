"""
Pytest Fixtures and Test Setup for Nexus SaaS Marketplace
"""

import os

# Clean host proxy environment variables to prevent SOCKS proxy errors when socksio is absent
for proxy_var in ["ALL_PROXY", "all_proxy", "HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy"]:
    os.environ.pop(proxy_var, None)

import pytest
from httpx import AsyncClient, ASGITransport
from app.core.database import Database
from app.core.clock import Clock
from app.main import create_app
from app.models.offers import OfferPricing


@pytest.fixture
def test_clock():
    """Controllable test clock initialized to a fixed UTC time."""
    from datetime import datetime, timezone
    fixed_time = datetime(2026, 11, 14, 10, 0, 0, tzinfo=timezone.utc)
    return Clock(initial_time=fixed_time)


@pytest.fixture
def test_db():
    """Fresh in-memory SQLite database per test."""
    return Database(":memory:")


@pytest.fixture
def app_and_services(test_db, test_clock):
    """Initializes app with test database, clock, and seeds baseline accounts."""
    app = create_app(db=test_db, clock=test_clock, enable_demo_mode=True)

    authority = app.state.authority
    accounting = app.state.accounting
    offers = app.state.offers

    # 1. Seed Owner (Alice) and issue owner key
    alice = authority.create_owner(email="alice@procurecorp.in", name="Alice Sharma")
    alice_key, alice_cred = authority.issue_owner_key(alice.id)

    # 2. Seed Agent (InvoiceBot)
    agent = authority.register_agent(alice.id, "InvoiceBot-01")
    # 3. Issue API Key
    raw_key, cred = authority.issue_agent_key(agent.id)
    # 4. Seed Wallet (5,000 test credits)
    accounting.seed_wallet(alice.id, 5000)
    # 5. Seed Spend Grant (1,000 max, 250 per order cap)
    grant = authority.create_spend_grant(
        owner_id=alice.id,
        agent_id=agent.id,
        max_allowance_credits=1000,
        per_order_max_credits=250,
        allowed_capabilities=["invoice.extract.v1"]
    )

    # 6. Seed Seller Owner (Bob)
    bob = authority.create_owner(email="bob@docuextract.com", name="Bob Tech")
    bob_key, bob_cred = authority.issue_owner_key(bob.id)
    seller = offers.register_seller(bob.id, "DocuExtract Solutions")
    
    # 7. Seed Offer (100 credits: 85 net, 15 fee, 30s deadline)
    offer = offers.publish_offer(
        seller_id=seller.id,
        title="High-Precision Invoice Extractor",
        description="Fast LLM-grounded invoice data extraction with exact character evidence spans.",
        buyer_total_credits=100,
        seller_net_credits=85,
        nexus_fee_credits=15,
        execution_deadline_seconds=30,
        endpoint_url="http://localhost:8000/sellers/deterministic",
        endpoint_secret="sec_seller_key_01"
    )

    return {
        "app": app,
        "db": test_db,
        "clock": test_clock,
        "alice": alice,
        "alice_key": alice_key,
        "bob": bob,
        "bob_key": bob_key,
        "agent": agent,
        "raw_key": raw_key,
        "grant": grant,
        "seller": seller,
        "offer": offer
    }


SAMPLE_INVOICE_TEXT = """
INVOICE
Billed By: Acme Industrial Supplies Ltd
Invoice Number: INV-2026-8841
Date: 2026-11-14
Currency: INR

Line Items:
1. Deep Groove Ball Bearings (Qty: 20) - ₹3,200.00
2. Replacement Solenoid Valves (Qty: 5) - ₹6,800.00

Subtotal: ₹10,000.00
GST Tax (18%): ₹1,800.00
Total Amount: ₹11,800.00
Payment Terms: Net 30 days
"""

