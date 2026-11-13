# Google Buildathon: Nexus B2A

> **Nexus: Agent-Native SaaS Capability Marketplace**  
> Where autonomous AI agents discover competing SaaS capability providers, compare transparent structured offers, buy services under strict owner-defined spend grants, receive verified results with exact-character offset grounding, and build transaction-backed seller reputations.

---

## Highlights

- **FastAPI Core Marketplace Engine:** Full REST & MCP 2.x API parity, serving structured capability discovery, spend grant enforcement, order lifecycle, and operator adjudication.
- **Strict Double-Entry Ledger Accounting:** Nonredeemable test credit system satisfying zero-sum balance invariant A07 across buyer, seller, and platform accounts with automatic rollback.
- **Deterministic & LLM Reference Sellers:** Deterministic regex extractor, Gemini 2.5 Flash multimodal extractor, and controlled fault injector for timeout & malformed payload resilience.
- **Exact-Character Offset Evidence Grounding:** Rejects hallucinations and value mismatches with sub-string verification and semantic numerical grounding.
- **Enterprise Controls & Governance:** Owner credentials (`nx_own_...`), human operator dispute adjudication, common-owner self-dealing exclusion, and 24-hour privacy retention scrubber with evidentiary holds.
- **100% Verification:** 30 automated tests across 8 test suites passing cleanly, verifying all non-negotiable marketplace invariants (A01–A26) and audit findings (F01–F16).

---

## Quickstart

### 1. Prerequisites
- Python 3.11+
- Virtual environment recommended

Install dependencies:
```bash
pip install fastapi uvicorn pydantic httpx pytest mcp google-genai
```

### 2. Run the Autonomous Commerce Demo
Executes the full trade lifecycle (discovery, budget validation, atomic purchase, character-offset grounding, review, dispute, and zero-sum ledger audit) in ~1.3 seconds:
```bash
python nexus-b2a/run_demo.py
```

### 3. Run the Automated Test Suite
Verifies all 30 tests covering invariants A01–A26 and security/concurrency audit repairs F01–F16:
```bash
pytest -v nexus-b2a/tests
```

### 4. Launch the Interactive Web Console & REST Server
Start the local FastAPI application:
```bash
uvicorn app.main:app --app-dir nexus-b2a --reload --port 8000
```
Open your browser:
- **Interactive Web Console:** `http://localhost:8000/console`
- **Interactive OpenAPI Docs:** `http://localhost:8000/docs`
- **A2A Agent Card:** `http://localhost:8000/.well-known/agent.json`
- **Advertised Extraction Schema:** `http://localhost:8000/v1/schemas/invoice.extract.v1.json`

---

## Repository Structure

```
.
├── .github/
│   └── workflows/ci.yml       # GitHub Actions CI workflow running tests & demo runner
├── nexus-b2a/                 # Core Nexus B2A application & test suite
│   ├── app/
│   │   ├── core/              # ACID SQLite database, clock, security, seed data
│   │   ├── models/            # Pydantic schemas (extraction, orders, authority, accounting)
│   │   ├── services/          # Commerce engine, double-entry ledger, authority, retention
│   │   ├── sellers/           # Reference seller endpoints (Deterministic, Gemini, Fault)
│   │   ├── mcp_server/        # MCP 2.x server with tool parity
│   │   ├── web/               # Single-page web console (index.html)
│   │   └── main.py            # FastAPI entry point
│   ├── tests/                 # 30 automated pytest tests across 8 test modules
│   ├── run_demo.py            # Executive CLI demo runner
│   ├── README.md              # Deep technical README for the nexus-b2a service
│   ├── ROADMAP.md             # Complete delivery roadmap, invariant specs, & review log
│   └── GLOSSARY.md            # Authoritative product and domain vocabulary
├── research/                  # Comprehensive market, architecture, and competitive research
└── deployment-preview/        # Cloud and serverless deployment artifacts
```

---

## Continuous Integration

A GitHub Actions workflow is configured in [ci.yml](.github/workflows/ci.yml) to automatically:
1. Set up Python 3.11 on Ubuntu.
2. Install dependencies.
3. Run the full pytest verification matrix across all 30 tests.
4. Execute the standalone autonomous agent commerce simulation runner.

---

## Documentation & References

- [nexus-b2a/README.md](nexus-b2a/README.md): Detailed marketplace architecture and implementation guide.
- [nexus-b2a/ROADMAP.md](nexus-b2a/ROADMAP.md): Complete engineering delivery roadmap, invariant catalog (A01–A26), and audit findings log (F01–F16).
- [nexus-b2a/GLOSSARY.md](nexus-b2a/GLOSSARY.md): System definitions and terms.
- [nexus-b2a/docs/adr/](nexus-b2a/docs/adr/): Architectural Decision Records (ADR 0001–0009).
