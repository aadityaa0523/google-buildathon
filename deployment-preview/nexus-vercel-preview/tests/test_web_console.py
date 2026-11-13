"""
Tests for Web Console and Public Demonstration Endpoints
"""

from starlette.testclient import TestClient
from app.main import create_app
from app.core.database import Database
from app.core.clock import Clock


def test_console_and_demo_endpoints():
    db = Database(":memory:")
    clock = Clock()
    app = create_app(db=db, clock=clock, auto_seed=True)
    client = TestClient(app)

    # 1. Health check JSON
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "OPERATIONAL"
    assert resp.json()["contract"] == "invoice.extract.v1"

    # 2. Console endpoint
    resp_console = client.get("/console")
    assert resp_console.status_code == 200
    assert "Nexus" in resp_console.text
    assert "Agent Purchase Tester" in resp_console.text

    # 3. HTML accept header on root
    resp_root_html = client.get("/", headers={"accept": "text/html,application/xhtml+xml"})
    assert resp_root_html.status_code == 200
    assert "<!DOCTYPE html>" in resp_root_html.text

    # 4. Demo Actor Endpoint
    resp_actor = client.get("/v1/demo_actor")
    assert resp_actor.status_code == 200
    data = resp_actor.json()
    assert "buyer_owner_id" in data
    assert "buyer_agent_id" in data
    assert "buyer_agent_key" in data
    assert "grant_id" in data
    assert len(data["offers"]) >= 3

    # 5. A2A Agent Card Discovery Endpoint
    resp_card = client.get("/.well-known/agent.json")
    assert resp_card.status_code == 200
    card_json = resp_card.json()
    assert card_json["name"] == "Nexus SaaS Capability Marketplace"
    assert "invoice.extract.v1" in [c["id"] for c in card_json["capabilities"]]

    resp_card_alias = client.get("/v1/agent-card")
    assert resp_card_alias.status_code == 200
    assert resp_card_alias.json()["name"] == "Nexus SaaS Capability Marketplace"
