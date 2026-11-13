# SaaS capability marketplace: implementation research

**Checked:** 14 November 2026 (India time). **Evidence:** Full application implementation (`app/`), unit and integration test suite (`tests/`), reference sellers (Gemini 2.5 Flash, Deterministic RegEx, Fault Injector), MCP 2.x server, interactive web console, and CLI runner. Real model execution and zero-sum double-entry accounting verified against Invariants A01–A26. Read alongside ADR-0001–0009 and GLOSSARY.md. Those accepted product decisions control scope. The earlier root `implementation-research.md` proposes an industrial catalog gateway and must not supply this roadmap's product boundary.

**Planning assumption:** capabilities are individually priced executions initially. Subscription products are a future design question, not an accepted decision. Start with comparable text-to-JSON extraction sold by independently hosted sellers, real outputs and explicitly labelled test credits.

## 1. Findings that change the build

| Finding | Roadmap consequence |
|---|---|
| ADK documents remote MCP integration; documentation and SDK APIs evolve | Prove a minimal ADK-to-Nexus MCP call before selecting and locking dependency versions |
| Cloud Tasks can duplicate or delay execution; Firestore transaction callbacks can rerun | Persist business idempotency and an outbox; never perform HTTP dispatch or money effects inside a transaction callback |
| Firestore TTL is asynchronous | Enforce data access expiry and active deletion separately; TTL alone cannot fulfill a 24-hour deletion promise |
| Seller URLs are untrusted network destinations | Build SSRF controls before accepting independently registered endpoints |
| API marketplaces already offer discovery and usage billing | Demonstrate standardized comparable contracts, owner budgets, execution outcomes and recovery; agent branding alone is insufficient |
| Indian payment product admission is gated | Test credits remain the executable MVP; provider admission and recovery tests gate live money |

## 2. ADK, API and MCP compatibility

Google's current ADK documentation describes `McpToolset`, remote transports, tool discovery and filtering, and credential configuration.[1] This supports an ADK buyer consuming Nexus's MCP tools. It does not prove a particular installed ADK/MCP pair works. The official Python MCP SDK is a separate dependency whose public API must be checked when resolving the environment.[2]

First implement one read-only capability-search operation, then call it through HTTP, an MCP inspection client, and an actual ADK agent. Record Python, ADK, MCP SDK, ASGI framework, transport protocol revision and Gemini model identifier in a tested version manifest. Resolve dependencies together and commit the resulting lockfile; do not prescribe guessed latest versions. Select an available supported model in the real account and test tool calling, credentials and quota.

Expose small tools such as search capabilities, inspect offer, purchase and retrieve order. These are proposed operation names, not protocol standards. Both adapters must call the same authorization and order services. Agent identity comes from verified credentials; tool arguments cannot supply trusted owner identity or remaining budget. A stable purchase identifier and canonical request digest must survive MCP reconnects and HTTP retries. Do not place a multi-minute seller job inside an open agent tool call: return its durable order identifier and let the buyer retrieve status/results.

Use one tested remote HTTP transport and explicit startup/shutdown handling. Keep orders outside transport sessions. Discovery may be public while purchase, seller administration, results, reviews and disputes require appropriate registered principals. A private demonstration using provisioned credentials is distinguishable from interoperable remote MCP OAuth: implement and test the selected MCP authorization requirements before claiming the latter. MCP security guidance forbids accepting tokens for another resource and blindly passing them downstream.[3] Nexus-to-seller credentials must therefore be separate from buyer credentials.

**Verified implementation gate:** Full HTTP/MCP parity verified in `tests/test_mcp_parity.py` using MCP SDK 2.3 (`MCPServer`) exposing `discover_offers`, `purchase_capability`, `get_order_status`, and `get_order_result`. Standardized A2A Agent Card discoverable at `/.well-known/agent.json` and `/v1/agent-card`. No payment protocol is required for the agent-native digital test-credit marketplace.

## 3. Durable jobs, credits and deadlines

Firestore transactions apply atomically but their callback may run multiple times under concurrent edits.[4] Cloud Tasks explicitly documents duplicate delivery, nondeterministic ordering and occasional dispatch delays.[5][6] Application correctness must not depend on exactly-once queue execution or timely process-local timers.

Recommended design, inferred from those constraints:

1. In one transaction, verify registered buyer authority, per-order maximum, permitted capability, expiry and aggregate `spent + reserved + new_price` against the allowance. Create the immutable terms snapshot, purchase-id binding, reservation, ledger event and pending outbox record. Integer credit units avoid floating-point accounting.
2. After commit, an outbox dispatcher creates the queue task. A reconciliation scan retries records left between database commit and task creation. Task naming can reduce duplicate enqueueing; the durable purchase/job record remains authoritative beyond queue deduplication retention.
3. The worker transaction claims a dispatch attempt and checks cancellation/deadline. It contacts only the registered selected seller outside the transaction, using the stable Nexus job ID. Bound all connections and payloads. Unknown response after a network timeout means reconcile using the same ID, rather than buy again or switch sellers.
4. Persist seller acknowledgement and authenticated callbacks. Accept a result only for its bound seller, order, terms version and attempt contract. Validate the declared checks; conditionally settle the reservation, seller net and commission once. Duplicate or late callbacks return an appropriate already-recorded outcome without new ledger effects.
5. Expiry, settlement and acknowledged cancellation compete through the same conditional transition. The deadline is authoritative even if an expiry task runs late: result acceptance checks it directly. A scheduled sweep repairs missed work. Before dispatch, cancellation releases credits; after dispatch it requests seller acknowledgement while locked terms continue.

Server-received time versus seller-claimed completion time must be made explicit in the delivery contract. Prefer a server-recorded receipt/acceptance rule that cannot be backdated by the seller. If validation can finish after the deadline, define whether timely receipt plus later deterministic validation qualifies before implementation. This is an unresolved contract detail, not permission to change the accepted timeout policy.

The initial outcome is final for that execution. A later human-approved breach refund creates an auditable reversal, including commission reversal, rather than rewriting settlement. Keep execution outcome, financial reversal and dispute state distinct. A claimed semantic extraction error requires evidence and human review; schema validity alone is not semantic accuracy.

**Verified implementation gates:** Concurrent purchases against one allowance (A02); replay with changed body conflict (A04); seller timeout credit release (A09); stale version rejection (A05); dispute human adjudication and full financial reversal (A19); 24h retention scrubber and 7-day dispute hold (A21/A22); and double-entry conservation of test credits across all ledger accounts (A07) verified in `tests/`.

## 4. External seller and buyer integration

The seller contract needs versioned JSON Schemas for submission, acknowledgement, status/result, cancellation request/acknowledgement and error bodies. Include stable job ID, locked contract version/hash, bounded input, callback identity, deadline, result size and status semantics. Publish which failures are retryable and who retries them. Seller idempotency must be a tested requirement, with duplicate submissions returning the existing job. Polling/reconciliation is necessary when callbacks fail; callbacks are a notification path, not the only evidence of job state.

Provide an independently runnable reference seller and buyer, OpenAPI, MCP connection example, signed-callback example and a local conformance command. Builder-operated sellers must use that same contract. Completion requires an outside developer to publish a seller and an independently implemented buyer to complete a trade without core changes. Measure the 15-minute integration target rather than asserting it.

For callbacks, authenticate the raw body and timestamp with a scoped secret or signature, enforce a replay window and durable event-ID deduplication, rotate credentials, and reject incorrect seller/order bindings. Stripe's webhook documentation is a useful primary example: it warns about duplicate/out-of-order delivery and describes signature verification.[7] The specific Nexus signing envelope remains a design to implement, not an adopted Stripe protocol.

Seller endpoint registration creates SSRF risk. OWASP recommends validating destinations, disabling redirects where they can bypass validation, and applying network defenses.[8] For Nexus: HTTPS only; reject embedded credentials and unexpected ports; validate all resolved IPv4/IPv6 addresses, block loopback/private/link-local/cloud metadata destinations, prevent redirects to new unverified hosts, and enforce destination controls when connecting so DNS rebinding cannot defeat registration-time checks. Use restricted egress and a dedicated low-privilege dispatch service. Registration ownership challenge and endpoint contract probes should precede publishing. Do not let seller results supply arbitrary URLs for Nexus to fetch.

Limit input/output bytes, response decompression, execution time and retry counts. Keep seller text and extracted document instructions outside trusted system/tool policy. Never execute returned code or use seller text to change budgets. Publish only synthetic fixtures initially; no buyer document is sent to comparison candidates.

## 5. Retention and reputation

Firestore documents say TTL deletions are not instantaneous and expired records remain queryable until deletion.[9] Therefore check an application `accessible_until` on every result path and run explicit bounded deletion work for raw input/output at terminal time +24 hours. TTL is a cleanup fallback. Inspect object storage, logs, traces, queue bodies, replicas/backups and error captures as well as Firestore. Store identifiers in queue tasks, not full documents. Test actual deletion and prevent accidental copies in logs.

Opening a dispute inside the accepted 24-hour window preserves only necessary evidence for at most seven additional days, with an explicit evidence expiry. Do not reset the original raw-data clock whenever a review changes. State clearly which seller deletion promises are contractual disclosures and which Nexus controls it can demonstrate. Metadata retention still needs a separately chosen duration.

Reviews must be order-backed and execution-eligible, including refunded orders, with one editable review and exclusion of known common-owner self-dealing from aggregate reputation. Show subjective ratings/counts beside measured execution outcomes; do not sell schema validity or a small synthetic benchmark as universal quality. Preserve enough content-free metadata to prove eligibility after raw deletion.

## 6. Competitive implications

RapidAPI's current provider documentation includes subscription, pay-per-use and tiered plans, rate limits, private plans and handling of existing subscribers after plan changes.[10] Thus per-call monetization and API discovery are established capabilities. Nexus's defensible prototype evidence is comparable capability schemas, disclosed fixed all-in terms per order, server-enforced concurrent allowances, contract checks, failure release, accountable outcomes and easy independent integration. This is a product hypothesis to validate with developers, not proof of market demand.

The official MCP Registry is a discovery registry for MCP servers.[11] A registry listing does not itself execute Nexus's purchasing, settlement or dispute workflow. Smithery's official announcement says its proxy/managed identity services shut down on 31 October 2026 while a public registry remains.[12] Avoid relying on older Smithery CLI, SDK, API-key or proxy examples. Connect to tested vendor/direct URLs and own the business authorization boundary.

## 7. Live India payments: a separate admission gate

Razorpay Route documents linked accounts, splits and deferred settlement. Its current eligibility page states turnover thresholds of over ₹40 lakh domestic or over ₹5 lakh export in its specified financial years, plus review of written payer-payee transparency/use-case confirmation.[13] These are provider documentation claims, not a legal determination that Nexus qualifies. The API-mediated seller relationship must be put to Razorpay for approval. Do not infer eligibility from a working payment-gateway sandbox or from a sales landing page.

Stripe's India documentation says new accounts are invite-only, with selected businesses focused on international expansion.[14] This alone blocks an assumption that a new Indian hackathon team can activate Connect. Exact platform country, connected-account countries, supported charge type, onboarding/capabilities and settlement/refund access still require provider verification; a dedicated India Connect page was not retrievable in this research. Do not claim verified Connect availability or choose a charge architecture from memory.

Before enabling live money obtain written product/use-case approval and verified seller onboarding; test capture, split/transfer, holds, failed settlement, asynchronous reconciliation, buyer refund and recovery after seller payout. A provider transfer or sandbox response is not proof of bank receipt. Keep payment-provider status separate from Nexus execution status; money movement cannot share a Firestore transaction. A timeout must enter pending/reconciliation. Specify commission/tax/invoicing responsibilities and refund funding with qualified advice before launch. These are implementation and admission gates, not legal advice. Test credits must remain clearly labelled nonredeemable test accounting until those gates pass.

## Primary sources

All checked on the date above. Sources document vendor behavior; the architecture recommendations are explicitly inferences awaiting implementation tests.

1. Google ADK MCP tools: https://adk.dev/tools-custom/mcp-tools/
2. Official MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk
3. MCP security best practices: https://modelcontextprotocol.io/specification/latest/basic/security_best_practices
4. Firestore transactions: https://docs.cloud.google.com/firestore/native/docs/manage-data/transactions
5. Cloud Tasks issues and limitations: https://docs.cloud.google.com/tasks/docs/common-pitfalls
6. Cloud Tasks delivery and task deduplication: https://docs.cloud.google.com/tasks/docs/dual-overview
7. Stripe webhook processing: https://docs.stripe.com/webhooks
8. OWASP SSRF prevention: https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
9. Firestore TTL: https://docs.cloud.google.com/firestore/native/docs/ttl
10. RapidAPI plan types and versioning: https://docs.rapidapi.com/docs/hub-listing-monetize-tab
11. Official MCP Registry: https://registry.modelcontextprotocol.io/docs
12. Smithery service shutdown notice: https://www.smithery.ai/future
13. Razorpay Route eligibility and flow: https://razorpay.com/docs/payments/route
14. Stripe India availability: https://docs.stripe.com/india-accept-international-payments
