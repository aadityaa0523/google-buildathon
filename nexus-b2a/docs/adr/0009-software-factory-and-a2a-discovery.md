# Software factory automation and agent-to-agent protocol discovery

Accepted during implementation. Nexus-B2A adopts the Software Factory architecture to govern continuous invariant verification, seller conformance testing, scheduled retention scrubbing, and autonomous agent trade simulations.

Work is organized into four discrete factory tasks running on disposable runners:
1. `verify-invariants`: Validates all 26 marketplace invariants (A01–A26) via automated test suites on every pull request and push to main.
2. `seller-conformance`: Probes newly registered seller endpoints with synthetic golden invoices, verifying `invoice.extract.v1` schema compliance and exact Unicode character evidence spans before activating catalog search visibility.
3. `ledger-retention-scrubber`: Hourly automated runner that purges expired payloads (past 24 hours, preserving dispute holds) and executes a full double-entry ledger audit verifying that every journal transaction and overall balance delta equals zero.
4. `run-commerce-simulation`: Standalone executive CLI runner executing the end-to-end autonomous buyer agent flow in under 2 seconds.

Three mandatory brakes prevent regression and uncoordinated execution:
- Automated checks: deterministic 12-suite pytest gates, strict Pydantic v2 validation, and OWASP SSRF destination address filter.
- Automated review: programmatic evidence span boundary checking, zero-sum journal verifier, and common-owner self-dealing exclusion.
- Human review: human owner authorization for spend grants, and operator console adjudication for disputed orders.

To ensure open discoverability across autonomous agent ecosystems, Nexus publishes a standardized Google/Linux Foundation A2A Agent Card at `/.well-known/agent.json` and `/v1/agent-card`. This exposes available capability IDs, endpoint protocols (REST, MCP 2.x SSE, and Web Console), authentication requirements (SHA-256 hashed bearer tokens with spend grant delegation), and double-entry governance rules without requiring human portal navigation.

