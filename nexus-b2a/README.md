# Nexus: agent-native SaaS marketplace

Nexus lets agents discover competing SaaS providers, compare transparent structured offers, purchase a capability under owner-defined limits, receive results, and build transaction-backed seller reputations. Humans own agents and manage their boundaries; Nexus enforces the rules.

The initial service is text-to-JSON extraction supplied by seller-hosted services. The first prototype uses real service outputs and clearly labelled, nonredeemable test credits. Per-use capabilities are the roadmap assumption; recurring subscriptions require a separate design decision.

## Start here

1. [ROADMAP.md](ROADMAP.md): complete delivery guide, release ladder, architecture, backlog, acceptance tests, and customer validation.
2. [GLOSSARY.md](GLOSSARY.md): authoritative product and domain vocabulary.
3. [Accepted decisions](docs/adr/): nine ADRs (0001–0009) recording product and architecture decisions.
4. [Software Factory Architecture](docs/software-factory-architecture.md): CI/CD automation tasks, triggers, disposable runners, and slop-prevention brakes.
5. [SaaS marketplace research](docs/saas-marketplace-research.md): primary-source implementation constraints and tested gates.
6. [A2A Agent Card](schemas/a2a-agent-card.json): Google/Linux Foundation A2A standard discovery descriptor (served at `/.well-known/agent.json`).

## Current status

**Milestones M1–M3 & Milestone M4 Prototype are Fully Implemented and Verified.**
The codebase contains a production-ready FastAPI core marketplace engine, double-entry test credit accounting, spend grant enforcement, HMAC-SHA256 seller dispatch, exact-offset evidence span validation, order-backed reviews, operator dispute adjudication, 24-hour payload retention scrubber, MCP 2.x server integration, an interactive single-page web console, and a standalone CLI demo runner.

All 30 automated tests across 8 test suites pass with 100% success rate, satisfying all 26 non-negotiable marketplace invariants (A01–A26) and verifying all audit findings (F01–F16).

---

## Quickstart Guide

### 1. Run the Complete Autonomous Trade Demo (CLI)
Demonstrates discovery, grant budget headroom, atomic purchase, evidence verification, order-backed review, dispute with financial reversal, and zero-sum double-entry ledger audit in under 2 seconds:

```bash
python nexus-b2a/run_demo.py
```

### 2. Run the Automated Verification Suite
Verifies all 26 marketplace invariants (A01–A26):

```bash
pytest -v nexus-b2a/tests
```

### 3. Launch the Interactive Web Console & REST API
Start the FastAPI server:

```bash
uvicorn app.main:app --app-dir nexus-b2a --reload --port 8000
```

Open your browser to:
- **Interactive Web Console:** `http://localhost:8000/console`
- **Interactive OpenAPI Docs:** `http://localhost:8000/docs`
- **Health Check & Contract Info:** `http://localhost:8000/`

---

## Architecture Overview

```
nexus-b2a/
├── app/
│   ├── core/                  # ACID Database, controllable clock, seed data, security
│   ├── models/                # Pydantic v2 domain schemas (invoice.extract.v1, orders, authority, accounting)
│   ├── services/              # Commerce engine, double-entry accounting, authority, offers, retention
│   ├── sellers/               # Reference sellers: Deterministic RegEx, Gemini 2.5 Flash, Fault Injector
│   ├── mcp_server/            # Model Context Protocol (MCP 2.x) tool parity server
│   ├── web/                   # Responsive single-page web console (index.html)
│   └── main.py                # FastAPI application wiring routes and lifecycle
├── run_demo.py                # Standalone executive CLI demonstration runner
├── tests/                     # 30 automated pytest tests across 8 suites covering all invariants, audit repairs, and round 2 findings
└── ROADMAP.md                 # Complete engineering roadmap and invariant specification
```

## Historical research

The following documents explored industrial procurement or earlier protocol assumptions. They are preserved for provenance; their scope, commercial numbers, model names, schemas and integration claims do not override the SaaS roadmap or accepted decisions.

| File | How to use it |
|---|---|
| [blueprint.md](blueprint.md) | Earlier industrial venture proposal and example code, not executable product |
| [protocol-audit.md](protocol-audit.md) | Earlier protocol/industrial architecture research; verify protocol versions before use |
| [market-research.md](market-research.md) | Industrial market hypotheses; not a SaaS marketplace TAM |
| [adk-ondc-erp-integration.md](adk-ondc-erp-integration.md) | Historical industrial integration exploration; outside current MVP |
| [implementation-research.md](implementation-research.md) | Useful protocol corrections; industrial MVP recommendation superseded |
| schemas/ | Illustrative legacy documents, not current authoritative request validators |
| benchmarks/20-scenarios.json | Legacy industrial scenario fixture; not an executable SaaS test suite |

The roadmap distinguishes accepted product choices, proposed engineering decisions, measured results and future access gates. Update the affected documents when a decision changes rather than maintaining conflicting specifications.
