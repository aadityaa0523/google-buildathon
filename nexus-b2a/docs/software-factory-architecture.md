# Nexus-B2A Software Factory Architecture

This document defines the Software Factory design for Nexus-B2A using canonical factory terminology (tasks, triggers, runs, runners, ticket trackers, orchestrators, and brakes).

---

## 1. Service Slots

Each service slot is filled with a specific product:

| Service Slot | Product / Implementation | Role in Nexus-B2A |
|---|---|---|
| **Ticket tracker** | GitHub Issues | Human interface for work scheduling, bug triage, capability requests, and operator audit reports. |
| **Ticket source** | Nexus Console Incident Webhook & Automated Ledger Auditor | Emits tickets upon unbalanced journal detection, failed SSRF attempts, or recurring seller SLA breaches. |
| **Git host** | GitHub | Stores branches, commits, PR reviews, and versioned schema contracts (`schemas/`). |
| **Orchestrator** | GitHub Actions | Listens to git host triggers, clocks, and webhooks; dispatches runs on runners. |
| **Runner** | Ephemeral GitHub Actions Linux Runners | Disposable compute environments executing tests, linting, and conformance suites. |
| **Observability platform** | GitHub Actions Run Logs + FastAPI OpenTelemetry traces | Surfaces per-run execution outputs, test logs, and ledger audit receipts. |

---

## 2. Factory Tasks and Runs

### Task 1: Invariant Verification (`verify-invariants`)
- **Trigger**: Pull request opened/updated, or commit pushed to `main`.
- **What it does**: Spins up disposable runner, configures isolated SQLite database, runs `pytest -v nexus-b2a/tests`, verifies zero-sum ledger audit and all 26 invariants (A01–A26).
- **Services read/written**: Reads repository branch; writes test results to GitHub check status.
- **What it triggers next**: If green, triggers automated review; if red, blocks PR merge.
- **Where a human re-enters**: Human reviews and approves PR once automated checks are green.
- **Deduplication guard**: GitHub Actions concurrency groups (`concurrency: ${{ github.workflow }}-${{ github.ref }}`) cancel superseded runs.

### Task 2: Seller Conformance Test (`seller-conformance`)
- **Trigger**: New seller offer registered or version incremented via API.
- **What it does**: Dispatches golden synthetic invoice vectors (`SAMPLE_INVOICE`) to the seller endpoint, validates `invoice.extract.v1` Pydantic v2 schema, and checks all Unicode character offset evidence spans.
- **Services read/written**: Reads seller endpoint; writes verification status to `sellers.verified_endpoint` in the database.
- **What it triggers next**: Activates offer in search catalog if passing; emits alert ticket if failing.
- **Where a human re-enters**: Seller operator updates endpoint if rejected; Nexus operator can review quarantined endpoints.
- **Deduplication guard**: Keyed by `(seller_id, offer_version)`.

### Task 3: Scheduled Ledger & Retention Scrubber (`ledger-retention-scrubber`)
- **Trigger**: Orchestrator clock cron (every hour: `0 * * * *`).
- **What it does**: Executes `retention.sweep_expired_payloads()` to purge records past 24 hours (preserving dispute holds), then computes `SUM(postings)` across the entire journal.
- **Services read/written**: Reads and mutates `payloads` and `journal` tables.
- **What it triggers next**: If any delta $\neq 0$ is found, writes an incident ticket to the ticket tracker.
- **Where a human re-enters**: Operator investigates any filed unbalanced ledger ticket immediately.
- **Deduplication guard**: Idempotent sweep query with database lock.

### Task 4: Autonomous Purchasing Agent Simulation (`run-commerce-simulation`)
- **Trigger**: Post-deployment trigger or manual workflow dispatch.
- **What it does**: Runs `python nexus-b2a/run_demo.py` end-to-end (discovery -> grant check -> purchase -> evidence check -> review -> dispute -> zero-sum check) in $< 2$ seconds.
- **Services read/written**: Reads live/staging API; writes test order records.
- **What it triggers next**: Reports smoke test result to orchestrator.

---

## 3. The Three Brakes (Slop Prevention)

1. **Automated Checks**:
   - `pytest -v nexus-b2a/tests` enforcing 12 test suites and 26 invariants.
   - Pydantic v2 strict schema validation on all inputs and outputs.
   - OWASP SSRF destination address filter.
2. **Automated Review**:
   - Evidence span boundary checker verifying `input_text[start:end] == snippet`.
   - Balanced journal transaction verifier (`verify_balanced()`).
   - Self-dealing detection excluding common-owner reviews.
3. **Human Review**:
   - Owner-defined spend grants requiring explicit initial human authorization.
   - Operator console adjudication for disputed transactions and refunds.
   - PR code reviews required before code touches production branches.

