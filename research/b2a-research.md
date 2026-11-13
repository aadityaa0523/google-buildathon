# Business-to-agent research: opportunities for an India-focused startup

Research date: 13 November 2026. Prepared for Aadityaa and Kanak; third founder profile pending. All opportunity rankings and business models below are hypotheses. Product pages establish positioning, not adoption or independently measured performance.

## 1. What B2A actually means

A business provides information, tools, transactions or real-world services that AI agents can discover and use on behalf of people or companies. The agent is usually the interface or technical user; the payer and legal principal are typically a human, business or agent platform. A traditional API becomes a better B2A product when agents can understand its capabilities, price, constraints and outcomes, and its operator can authenticate, authorize, monitor and bill calls. An MCP wrapper by itself is not a defensible business.

Example: a factory purchasing agent receives a request for a motor bearing. It queries supplier services for matching part number, available stock, delivery date, price and tax, cites responses and presents a comparison. The authorized employee approves a quote. The value is accurate sourcing and saved procurement time; the agent-accessible interface is the delivery mechanism.

## 2. Market map: eight angles

| Angle | What is sold and who pays | Specific need / first product | Existing activity and risk |
|---|---|---|---|
| Agent-ready commerce | Merchant pays for exposure or tools; platform may pay usage | Accurate, structured availability, price, product specs and fulfilment data | Google UCP supports commerce journeys; ONDC already digitizes seller catalogues. Differentiation must be a particular vertical and data quality. |
| Specialist data / tools | Agent developer or enterprise pays per call or subscription | Reliable regional-language, industrial, logistics or public-source data with provenance, freshness and licensing | Coinbase Bazaar already lists paid endpoints; generic API marketplaces have discovery and distribution problems. |
| Agent-to-business workflows | Supplier or purchasing team pays | Capture RFQs, normalize supplier responses and issue verified quotes through a structured tool | Procurement suites and marketplaces already exist; win on access to a narrow supply base and actual quote accuracy. |
| Agent-to-human fulfilment | Enterprise agent operator pays for completed job | Dispatch a vetted technician to inspect equipment and return structured evidence | Field-service platforms and gig networks already exist; onboarding, liability and quality of service dominate. |
| Trust / delegated authority | Enterprise agent operator pays | Define scoped permissions, spend limits, approvals and auditable actions | AP2 and established payment/identity providers cover parts of this; a universal identity protocol is a poor hackathon bet. |
| Reliability and evaluation | Teams deploying agents pay | Test real tasks against adversarial inputs, stale data, costly errors and regression cases | Existing observability/evaluation products are competitors; differentiation requires domain-specific benchmarks and outcomes. |
| Discovery and ranking | Merchants or agent platform pays | Measure whether agents find accurate answers from a merchant catalogue and identify information gaps | Platforms can change ranking or incorporate features; no one can guarantee another agent recommends a seller. |
| Post-transaction operations | Merchant, operator or enterprise pays | Track order confirmation, delay, cancellation, refund and dispute evidence | Existing commerce systems already handle parts; strongest value is a narrow cross-system failure such as reconciliation of quote vs delivery. |

## 3. Real protocols and what they do

- **MCP** connects an agent host to tools and context. Tool descriptions are untrusted hints; they are not access control or proof of safety. [MCP security discussion](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/).
- **A2A** standardizes communication and task handoff between agents; discovery can be advertised through an agent card. Use when two independent agents genuinely need to collaborate, not just to make an ordinary API call look impressive. [Google developer guide](https://developers.googleblog.com/en/developers-guide-to-ai-agent-protocols/).
- **UCP** provides commerce primitives across discovery, shopping and checkout and supports different integrations. A prototype using a mock API is not automatically UCP-compliant. [Google UCP overview](https://developers.googleblog.com/under-the-hood-universal-commerce-protocol-ucp/).
- **AP2** supports payment authorization using mandates and can work with UCP/A2A. A Google codelab demonstrates a signed mock purchase and explicit user confirmation. [AP2 documentation](https://github.com/google-agentic-commerce/AP2/blob/main/docs/index.md); [codelab](https://codelabs.developers.google.com/next26/adk-agent-commerce).
- **x402** enables payment-gated HTTP/tool resources in certain implementations. Coinbase documents discovery of paid endpoints; do not assume a crypto payment method is suitable for Indian users or commercially/legal appropriate. [Coinbase documentation](https://docs.cdp.coinbase.com/api-reference/v2/rest-api/x402-facilitator/bazaar-mcp-server).
- **ONDC** is an Indian commerce network with defined buyer/seller participant responsibilities, rather than a generic open endpoint free of onboarding. Its buyer network description explicitly includes voice assistants and chatbots as possible interfaces. [Buyer participants](https://www.ondc.org/pages/buyer-network-participants.html); [seller participants](https://ondc.org/pages/seller-network-participants.html). UCP and ONDC are different systems; interoperability needs integration and is not assumed.

Payment claims change quickly. [Pine Labs announced P3P](https://www.pinelabs.com/media-analyst/the-ai-agent-can-now-pay-pine-labs-launches-p3p-indias-first-agentic-payment-protocol-built-on-upi) in June 2026 with a claim of autonomous UPI payment in production. This is a vendor claim; it does not establish universal availability or regulatory coverage. Verify partner access, applicable rules, consent and authentication before building real payments.

## 4. Product ideas for this team

### A. Agent-ready industrial sourcing desk — leading candidate

**User / payer:** purchasing manager at a small manufacturer, or a distributor that handles frequent parts inquiries. The agent is the interface; the distributor or purchasing organization is the potential subscriber.

**Problem:** a purchasing workflow may involve inconsistent part descriptions, catalog PDFs, stock and delivery constraints. This is a concrete hypothesis, not proof of unmet demand; interview real buyers and distributors. General evidence of SME process and AI adoption barriers appears in the [PSA/WEF India SME playbook](https://www.psa.gov.in/CMS/web/sites/default/files/publication/WEF_Transforming_Small_Businesses_2025.pdf).

**Product:** accept a part number, photo of a label, voice note or structured RFQ; normalize manufacturer, model, dimensions, quantity, delivery location and requested delivery date. Query two mock distributor services. Return matched alternatives with source, quote timestamp, stock freshness and explicit unknowns. Flag ambiguity and have a human approve an RFQ or order. The buyer owns the criteria; paid placement must be disclosed and not silently override them.

**Why B2A:** supplier quotes are exposed to an agent through structured, permissioned tools; a human-facing interface can use the exact same data. Today it can help sales staff answer inquiries even without independent purchasing agents. Future agent usage is upside, not required to justify a pilot.

**Competition:** IndiaMART and Moglix offer industrial sourcing today; existing enterprise procurement tools manage quote workflows. [IndiaMART](https://www.indiamart.com/); [Moglix](https://www.moglix.com/). UCP and ONDC are enabling standards/ecosystems, not proof a particular industrial niche is empty. Proposed wedge: high-precision compatibility and freshness for one part family, plus a distributor-assisted quote workflow. Validate competitor features and stock coverage in the target city.

**Two-day MVP:** use synthetic catalogue data for 30 SKUs and two suppliers; Gemini extracts fields from a synthetic label/photo and RFQ; deterministic rules match part numbers, units and constraints; FastAPI provides a typed read-only tool; React displays comparisons with sources and timestamps. Simulate quote request and confirmation. Host on Google Cloud if access and credentials permit; otherwise clearly label local demonstration. Use 20 held-out test RFQs including ambiguous, expired and incompatible items; measure exact-match accuracy, unsupported recommendations and human review time. Never present simulated data as live inventory.

**Business model:** hypothetical monthly distributor subscription or per qualified RFQ; potential buyer-side subscription for sourcing teams. First obtain evidence of willingness to pay. A transaction fee needs reliable attribution and aligned incentives.

**Risks:** wrong replacement parts and outdated stock can cost customers; disallow confident substitution without verified compatibility, expose expiry and require approval. Supplier data acquisition, low response rates and onboarding are the actual commercial bottlenecks. Founders' EEE/ECE, industrial exposure, CV and FastAPI fit implementation; personal access to relevant suppliers remains unverified.

### B. Agent-ready field-service handoff

**Problem hypothesis:** a remote maintenance agent can flag a fault but cannot inspect the physical equipment. A service coordinates human inspection, then returns a structured, timestamped report and authorized images to the requesting workflow.

**Buyer:** equipment service company or industrial facility; provider is a vetted technician. **Demo:** synthetic pump incident -> scope/availability -> simulated technician acceptance -> image and checklist -> cited status for requesting agent. No real dispatch required. **Competition:** field-service management vendors already schedule technicians; validate what they cannot expose as an agent tool. **Risk:** physical service quality, travel, dispute resolution and insurance. This needs supply and operations, not merely software. Team's embedded/industrial exposure helps, but does not establish a service network.

### C. Agent readiness and verification for Indian product catalogues

**Buyer:** a distributor, ONDC seller participant or D2C operator. **Need hypothesis:** inconsistent catalogues and stale availability reduce the ability of human and agent channels to answer product-specific questions. Upload sample product documents; extract attributes with citations, flag missing size/unit/availability information and export an API-ready catalogue after human review. Test with a set of buyer queries, reporting answerability and field accuracy. Charge a catalogue onboarding fee plus subscription only if customers validate value. Google, Shopify, ONDC seller tools and commerce platforms already provide related functions; focus on a specific catalogue type, languages, and evidence freshness. Do not promise search ranking or UCP/ONDC certification.

### D. Agent action assurance for one workflow

**Buyer:** a business deploying a purchasing, accounting or customer-support agent. Evaluate tool calls against a defined policy, require approval for sensitive actions, and record requested action, input source, decision and result. Demo an adversarial supplier description that attempts to alter a spending limit; deterministic policy rejects it and shows why. Also test normal approved cases and revoked credentials. Charge per protected workflow or usage. Strong engineering fit, but established security vendors, cloud platforms and framework features create significant competition. A demo policy engine is not a security guarantee. Google describes indirect prompt injection risks from external data: [Google Cloud guidance](https://docs.cloud.google.com/data-agent-kit/prompt-injection-risk?hl=en).

### E. Agent evaluation service for Indian-language workflows

**Buyer:** enterprise building customer-service or commerce agents. Create a consented test set of code-switched speech/text and realistic tasks for a narrow domain; grade factual extraction, escalation and tool usage with human-reviewed labels. Offer a report and regression test suite. Team's benchmark and ML evaluation experience fit well. However, agent evaluation vendors and model providers already compete; access to representative data and qualified annotators is the moat hypothesis, not the word 'benchmark'. Never claim general language coverage from a small dataset.

## 5. Scoring and selection — qualitative, not market facts

| Candidate | Founder fit | Speed to convincing demo | Path to paying customer | Dependency |
|---|---|---|---|---|
| Industrial sourcing desk | High | High with mock catalogues | Medium, if team can reach distributors | supplier data and reliable product matches |
| Field-service handoff | High | Medium | Medium | actual technician network and service quality |
| Catalogue readiness | High | High | Medium | differentiated data access; platform competition |
| Action assurance | High | High | Uncertain | credibility and competitive security market |
| Indian-language evaluation | High | Medium | Medium | authentic datasets and evaluator access |

Rank is conditional on who the team can interview. If you have direct access to factory quality managers but not distributors, the previously proposed quality workflow may be superior; forcing agent-to-agent communication into inspection is not necessary. If you can access distributors, the sourcing desk offers a better B2A story.

## 6. Evidence and research gaps

Platform investments and specifications show ecosystem activity, not a proven count of paying B2A customers, autonomous shopping volume or profitable startup demand. Company-reported figures and press releases should not be treated as independent performance evidence. No market sizing estimate or revenue forecast is justified by this scan. Interviews and competitor demonstrations are required before claiming whitespace.

Interview 3 purchasing staff, 3 industrial distributors and 2 agent developers. Ask about the last order, catalogue format, time to obtain a quote, errors and who approves purchases; request permission to observe and use redacted samples. For each alternative ask whether a customer would pay for the underlying workflow today. Test a prototype with 10 real but consented/redacted RFQs. Measure correct matches, unknowns correctly surfaced, false matches, freshness and comparison time. Seek a written pilot expression of interest; do not present interest as a contract.

**Security and operations:** separate untrusted documents from system instructions; implement authentication, least privilege, deterministic authorization checks, idempotency and audit logging; allow human review for quotes and transactions. Treat prices, availability and compatibility as time-bound source claims. Payment, ONDC production membership and security certification are outside this mock demo.
