# Ranked top five: buildathon ideas

13 November 2026. This supersedes earlier recommendations for this shortlist, while preserving earlier research. Ranking is editorial judgment based on the two CVs, user interest, scope for a convincing two-day demonstration, and potential business value. These are hypotheses, not validated gaps or claims of being first in India. No customer interviews, quotes, partnerships or willingness-to-pay tests have been conducted. The third CV is pending.

## Filter used

- Name the customer and transaction or physical outcome.
- Explain the work beyond producing an AI answer: instrumented tests, execution, physical fulfillment, or accountable transactions.
- Identify closest alternatives; an India label, local language, QR code or AI interface alone is insufficient differentiation.
- Demonstrate the uncertain hard part with a meaningful baseline, not a polished dashboard alone.
- Separate prototype feasibility from operating a viable company. Rankings 4 and 5 are notably conditional.

## 1. Agent service marketplace with verifiable delivery

**Pitch:** Give an agent a spending limit and let it purchase a narrowly specified service from competing providers, check agreed delivery conditions, and handle failure under an explicit contract.

This develops the user's B2A idea. Start with one service category, such as structured extraction from permissioned product catalogues. A buyer specifies required fields, permitted sources, volume and deadline. Providers publish machine-readable offers. The product handles discovery, bounded authorization, invocation, output checks, receipts and retry/dispute states. Charge a transaction or orchestration fee if buyers value the reliability enough to cover it.

**What exists:** [Coinbase Bazaar's MCP server](https://docs.cdp.coinbase.com/api-reference/v2/rest-api/x402-facilitator/bazaar-mcp-server) already exposes search and paid endpoint invocation. [Base's agent page](https://www.base.org/agents) describes paid API discovery and monetization. Discovery/payment is not our invention. Proposed advantage: category-specific acceptance tests and comparable evidence of delivery. This is not established whitespace; further competitor discovery is necessary, including service testing, routing and dispute providers.

**Two-day proof:** Three controlled providers, one returning incomplete data and one failing; the buyer selects a service, enforces a budget, checks outputs, and retries only with remaining authorization. Use simulated credit/payment states clearly labelled. Distinguish syntactic checks from truth: schema validity does not establish factual accuracy. Compare against simply calling the cheapest provider; report completion, cost and false acceptance on held-out labelled inputs.

**AI role:** Gemini maps a request into a typed specification and explains offer tradeoffs; explicit rules enforce budgets and acceptance conditions. The model cannot unilaterally approve spending beyond the user's authorization or certify its own output as true.

**Why it ranks first:** Strong alignment with user interest and agent/full-stack experience; a complete software demonstration is possible. **Kill condition:** buyers prefer direct APIs or verification costs more than the failure it prevents. Seller adoption and actual agent demand remain unproven. Real fund custody, refunds and payment-provider arrangements are separate work from a simulated demo.

## 2. Practical-skills coach for one vocational training task

**Pitch:** An apprentice performs a physical task in front of a phone; the product tracks a reviewed sequence, spots visible missed steps and produces evidence an instructor can review.

First customer hypothesis: a private vocational institute or repair-training centre. Start with one benign assembly exercise on an unpowered training fixture. Instructor approves the reference demonstration and observable checkpoints. The learner receives local-language guidance, while uncertain or occluded steps are explicitly marked unverified. Proposed revenue: institute subscription or per learner cohort.

**What exists:** [DeepHow](https://deephow.com/) already advertises expert knowledge capture, visual inspection and live SOP verification. [Augmentir](https://www.augmentir.ai/lp/connected-worker-platform) combines frontline skills, work instructions and training. The technical category is established. The proposed adaptation is an inexpensive, instructor-supervised practice station for small Indian training centres, rather than a broad enterprise rollout. It is unproven that current providers cannot serve this segment or that institutes will pay.

**Two-day proof:** One five-step assembly, a reference recording, and held-out learner attempts with a skipped step, wrong orientation and camera occlusion. Track state across the session; compare a generic live-video assistant against the constrained checkpoint system. Report missed errors and false alerts. Instructor reviews the evidence, not an opaque competence score. No claim of formal certification or autonomous safety supervision.

**AI role:** Gemini helps structure instructor-approved instructions and provides multilingual feedback; visual/state checks identify only supported observations. Don't infer torque, electrical safety or internal condition from appearance.

**Why it ranks second:** Strong CV/Android fit and an immediately understandable physical demo. **Kill condition:** no improvement over a recorded video plus instructor checklist, or institutes lack budget/interest. Founder access to an institute is unknown.

## 3. Recreate unavailable, simple spare parts

**Pitch:** A repair shop gets a discontinued plastic knob or clip reproduced locally, with a measured design and a record that can be reused for the next order.

Start with one non-safety-critical part family and a local fabrication partner. Gather photos, dimensions and material requirements, check an existing catalogue, prepare a reviewed design, manufacture a sample and record the fit result. Charge design/setup plus fulfillment, with repeat orders reusing the approved model. This extends beyond the previously proposed repair-parts lookup: the output is a made and checked physical replacement.

**What exists:** [Replique's engineering services](https://replique.io/en/engineering-services/) include CAD reconstruction from drawings or physical samples, and [its spare-parts offering](https://replique.io/en/spare-parts-and-urgent-demand-on-demand/) combines design support and on-demand manufacturing. [Nyris and Replique](https://www.nyris.io/blog-posts/nyris-and-replique-announce-their-spare-parts-on-demand-service) already describe photo search followed by manufacturing. This is an overseas precedent, not proof India lacks suppliers. Local CAD bureaus, 3D-print shops and repair markets are important direct substitutes that still require investigation.

**Two-day proof:** One owned or authorized sample, caliper measurements, a constrained parametric CAD template, human-reviewed dimensions, and a printed replacement whose fit can be demonstrated. A catalogue of three designs is sufficient; universal photo-to-functional-part generation is not. If fabrication access cannot be secured, this candidate drops sharply.

**AI role:** Interpret intake photos/notes, flag missing dimensions and select a candidate design template. Measured geometry, material decisions and approval control production. No claim that a photo reveals material strength or exact tolerances.

**Why it ranks third:** Tangible outcome and potential reusable inventory; requires CAD/manufacturing expertise not established by the CVs. **Kill condition:** setup/inspection costs exceed the customer's alternative, or demand is too fragmented to reuse designs. Permission/IP and technical suitability must be checked for actual parts.

## 4. Assisted used-phone handover verification

**Pitch:** Two people trading a used phone get a fresh functional and condition check at handover, with both parties seeing the same time-bound evidence.

Start in one campus or neighbourhood with an independent repair-shop partner. Buyer books a check; the seller brings the phone; supported diagnostics and guided cosmetic photos are captured; buyer sees limitations before accepting the sale. Charge per inspection. Initially buying or integrating existing diagnostics may be more sensible than developing them.

**What exists:** [Phonecheck](https://www.phonecheck.com/device-certification) already offers hardware/lock/history testing and per-device reports; its [QR-linked certification](https://www.phonecheck.com/newsroom/new-phonecheck-label-features-qr-code-to-device-history-report) predates this idea. [Cashify](https://www.cashify.in/buy-refurbished-mobile-phones) sells inspected refurbished phones. A shareable passport or QR code is not a differentiator. Hypothesis: one-off peer sellers want an accessible local service without selling the phone to a reseller. Need check whether Phonecheck providers or Indian shops already serve them effectively.

**Two-day proof:** Two Android devices, supported touch/camera/microphone/sensor tests, guided cosmetic capture, fresh buyer-side retest and a report with explicit untested items. No invented IMEI, stolen-status, financing, OEM-parts or battery-health verification; some require licensed sources, privileged software or specialist tools. A signed report proves record integrity, not that a dishonest tester used the claimed device.

**AI role:** Guide capture and summarize discrepancies; instrumented tests and human inspection provide underlying evidence.

**Why only fourth:** Relatable consumer value and Android fit, but heavy competitive overlap and weak AI necessity. **Kill condition:** buyers won't pay, trustworthy checks require uneconomic hardware, or an established service already offers the same handover experience. This is more a distribution/service hypothesis than a new diagnostic technology.

## 5. Traveler shopping marketplace, narrowed to unavailable products

**Pitch:** Match a shopper seeking a specific overseas item with a traveler on one route, showing the full proposed cost, purchase evidence, handover terms and a clear failure process.

Retains the user's idea. Focus on availability and a dense trusted community rather than assuming every US phone is cheaper. Proposed revenue: a completed-transaction service fee. No live pilot until the intended import and payment mechanisms are established.

**What exists:** [Grabr](https://grabr.io/en/how-grabr-works) already describes the matching, traveler purchase, reward and payment-hold workflow. Prior research identifies India-focused alternatives too: see [traveler-marketplace.md](traveler-marketplace.md). India is not an empty market.

**Two-day proof:** Synthetic shopper/traveler profiles, route/date matching, exact model comparison, an illustrative cost sheet with unresolved costs marked, simulated purchase evidence and handover/dispute states. Gemini parses product variants and presents sourced comparisons. This demo does not establish lawful paid carriage or operational viability.

**Why fifth:** Strong personal problem insight and clear story, but weaker Google AI depth, direct competition and unresolved cross-border operations. **Kill condition:** no workable permitted route or no advantage after total costs and risk. See the prior legal sources and limitations in the dedicated brief; no new legal determination made here.

## Ideas removed during this pass

- **Generic Indian voice-agent chaos testing:** [Hamming's workflow testing runbook](https://hamming.ai/resources/voice-agent-workflow-testing-runbook) explicitly checks tool calls and backend state, including missing/duplicate bookings. Adding backend evidence to multilingual testing is not a demonstrated gap.
- **Small-batch factory capacity marketplace:** [Xometry](https://www.xometry.com/start/) and [Zetwerk](https://www.zetwerk.com/en-us/capabilities/prototyping-and-preproduction/) already market small-quantity production, quoting and manufacturing assistance. The research did not establish the proposed generic feature bundle as distinctive.

See [competition check](top-five-competition-check.md). Where its summary is softer than the detailed primary-source findings, use the direct evidence above: neither removed idea should be pitched as new.

## Decision

First investigate #1 with agent developers and #2 with one vocational instructor. Choose #1 for the most self-contained software prototype; choose #2 if a training centre will supply a task and review attempts. #3 needs immediate fabrication access. #4 and #5 remain conditional options, not equally strong recommendations. No claim that novelty alone wins: the useful lesson from comparable winners is to demonstrate a complete, testable outcome. Event wins do not validate the market.
