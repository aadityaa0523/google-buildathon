# Long-term startup decision: market and repeat revenue first

Date: 13 November 2026. The user reports a one-week event extension and prioritises a large, durable business beyond the buildathon. Deadline and founder CV matching are not selection filters. The extension was not independently verified in this pass.

## Recommendation

**Lead hypothesis: an AI-assisted industrial spare-parts purchasing network for small and midsize factories.** Turn an incomplete part request into a correctly specified, supplier-confirmed and fulfilled order. Begin with one component family in one industrial cluster; expand through repeat purchasing and adjacent supplies.

This supersedes the audio-description recommendation for the revised long-term objective. Audio description remains a specialised product candidate; we have not established sufficient reachable commercial demand to rank it first for a large company. Neither idea has been validated by our customer interviews or sales.

Industrial procurement is an operating business supported by software. Supplier relationships, domain knowledge and fulfilment matter as much as AI. Building a durable company will require substantially more work than modifying a hackathon demo.

## Why this category

Grainger reported $17.942 billion in 2025 sales and $2.495 billion operating earnings. This demonstrates a large business around maintenance, repair and operating supplies. It is a global distributor's revenue, **not India's TAM, platform commission revenue or our obtainable market**. [Grainger results](https://invest.grainger.com/investor-news/news-details/2026/GRAINGER-REPORTS-RESULTS-FOR-THE-FOURTH-QUARTER-AND-FULL-YEAR-2025/default.aspx)

India already has major competitors: IndustryBuying describes over one million catalog products and 1.5 million business customers (company claims, not independently verified active buyer counts). Moglix offers procurement services and Cognilix sells source-to-pay, vendor management and inventory planning. [IndustryBuying](https://prod.industrybuying.com/about-us), [Moglix](https://business.moglix.com/about-us), [Cognilix](https://www.cognilix.com/).

A defensible current India TAM was not established here. Estimate the initial obtainable market from real factories in a cluster, relevant purchasing records, attainable order share and actual margin. Do not multiply all MSMEs by speculative spending.

## Customer and proposed product

Illustrative request: a maintenance buyer has a photo of a worn transmission belt, partially legible markings and a machine model. They need the approved replacement, actual availability, an invoice and a credible delivery time.

1. Accept images, part numbers, old invoices, drawings and voice notes.
2. Gemini structures the request, retrieves catalog evidence and asks for missing specifications. Deterministic checks compare required fields.
3. A knowledgeable supplier and the buyer's maintenance team confirm the exact item. Begin with approved exact replacements; visual similarity does not establish compatibility.
4. Participating distributors confirm stock, price, provenance, terms and dispatch time. Published stock is not treated as confirmed stock.
5. The buyer approves an order; the operation coordinates fulfilment, invoicing, returns and follow-up.
6. Permissioned purchase and outcome history makes subsequent orders easier to process.

Choose one bounded family, such as specified industrial belts, after buyer discovery. Whether a part is safety-critical depends on its application. Exclude applications requiring specialised certification or unverified substitutions initially.

## Competitive advantage to test

Photo-based identification already exists: nyris offers image/text/OCR-assisted catalog search. AI sourcing vendors and Moglix cover substantial procurement workflows. The hypothesis must therefore be transactional: **can we get buyers an approved part with better confirmed availability, delivery or total purchasing effort than their current route?** [nyris](https://www.nyris.io/), [Sidrun](https://sidrun.ai/), [Cognilix](https://www.cognilix.com/).

Local language, AI and a chat interface are insufficient differentiation. Potential advantages to earn are reliable local supply coverage, repeat purchasing relationships, verified application history, supplier performance records and concentrated delivery routes. Existing distributors may already possess these. We have not established an underserved cluster from public sources.

## Business model and scale

Start with a disclosed sourcing fee/commission on fulfilled orders, or an explicitly defined resale model. Use distributor inventory initially. Commission revenue and gross merchandise sales are different accounting models; do not conflate them.

Illustration only: 1,000 factories routing Rs 1 lakh/month produces Rs 120 crore annual order value. At an assumed 8% commission, revenue would be Rs 9.6 crore/year before delivery, returns, staff, support, payment costs and other expenses. No customer count, spending, capture or commission assumption is validated. Reselling as principal has different revenue and cost-of-goods treatment.

Expansion path: prove repeat orders and contribution in one category/cluster; add adjacent supplies using the same relationships; introduce scheduled replenishment and multi-site controls; replicate the operation in other clusters. Credit and broad inventory ownership are optional later decisions with substantial capital implications.

A permissioned ordering API could eventually let business agents buy from the same network. This retains the user's B2A interest while starting with existing human-led demand. Agent purchasing is an expansion hypothesis, not a prerequisite for the initial business.

## Comparison

| Direction | Long-term assessment |
|---|---|
| Industrial spares purchasing | Lead: repeated existing spend and adjacent expansion; operational and competitive burden is substantial |
| Commercial HVAC contractor software | Strong software-oriented alternative: recurring jobs and an identifiable owner; Indian willingness to pay and advantage over Zoho FSM need proof |
| Export operations | Large underlying trade flow, but document-heavy workflows are crowded; lower priority without a particular exporter access advantage |
| Generic agent-service marketplace | Active competitors; recurring paying demand and two-sided acquisition remain less established in our research |
| Audio-description review | Plausible specialised product; reachable revenue and comparative quality advantage unverified |

ServiceTitan illustrates the alternative's global potential: FY2026 revenue was $961.0 million, including $925.4 million platform revenue; its $82.1 billion gross transaction volume is separate. These are not India demand estimates. [ServiceTitan results](https://investors.servicetitan.com/static-files/ea7612c3-9088-4c98-88de-7fa172b80aea). Zoho already offers extensive field-service workflows. [Zoho FSM](https://www.zoho.com/fsm/features.html)

## Four-week commercial test

This is a proposed plan, not completed validation:

- Interview ten maintenance/procurement buyers and five verifiable distributors in one cluster. Inspect recent difficult orders, actual value, timing, credit terms and current alternatives.
- Obtain permission to analyse roughly twenty past requests. Find one recurring category where the current route is measurably weak; compare an incumbent where possible.
- Run a small manually assisted sourcing pilot with real new orders, explicit approvals and distributor stock. Track conversion, fill rate, delivery, returns, staff minutes and contribution per order.
- Seek repeat purchase without continual discounts. Determine whether the actual problem is identification, availability, price, credit or delivery; AI helps some more than others.

Stop or change direction if existing channels already satisfy buyers, the main demand is credit we cannot provide, suppliers cannot confirm reliable stock, or support/delivery consumes the margin. Positive interviews alone are insufficient.

## Buildathon scope

Demonstrate incomplete request → structured specification → evidence-backed exact-match shortlist → supplier confirmation → comparable quotes → approved order. Gemini supplies extraction and catalog reasoning; Google Cloud hosts the application and order state. Label mock suppliers, stock and payments. Technical feasibility is distinct from commercial proof.

Companion reports: [industrial procurement](large-market-industrial-procurement.md), [service contractors](large-market-service-businesses.md), [independent export alternative](large-market-independent-challenge.md), [agent marketplace validation](agent-marketplace-validation.md).
