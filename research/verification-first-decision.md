# Verification-first opportunity screen

Research date: 13 November 2026. User requested new ideas only after competitive verification and rejected the industrial-parts network as already implemented. This document supersedes earlier recommended lists for the current decision.

## Outcome

**No candidate in this pass clears both a convincing unmet-product gap and verified willingness to pay for the proposed implementation.** One narrower engineering opportunity merits further investigation, described below. Do not turn the negative findings into another confident list of supposedly original businesses. A bounded public-source search cannot prove that a product does not exist, and website feature descriptions cannot substitute for hands-on competitive testing.

## One conditional candidate: warranty-informed physical redesign

Sell appliance manufacturers a tool that proposes specific, costed product-design changes to reduce future repair expense. For a product revision, connect field failure frequency and actual repair steps/cost with the CAD assembly. Generate constrained alternatives such as a replaceable connector, an accessible pump or a separately removable control module. Compare added manufacturing/tooling cost against expected savings using the customer's installed-base and failure assumptions. The output is a proposed engineering change, its geometric checks, service procedure and sensitivity analysis.

Illustrative example: a frequently failing connector is part of an expensive sealed assembly. Evaluate a removable connector module against the current design. A proposal must preserve explicit engineering constraints; service access, sealing, strength and manufacturability need engineering review. LLM-generated geometry or confident text is not evidence that the change is feasible.

### What was verified

- Manufacturers purchase repairability advice: iFixit explicitly describes paid OEM consulting and assessments. This supports the existence of spending on the job, not a budget for this software. [iFixit partnerships](https://www.ifixit.com/Info/Our_Partnerships)
- Warranty expense is a material cost category. Whirlpool's FY2025 report includes $218m product-warranty issuances/accruals and $214m settlements/other in its reserve roll-forward. These are one company's accounting figures, not our market size or avoidable savings. [Whirlpool report](https://ar.whirlpoolcorp.com/Whirlpool_2025_AR.pdf)
- Broad service-to-design analytics already exists. PTC Orbit unifies product and field/service records and applies AI for engineering, quality and service. Generic warranty analytics or connecting claims to a CAD model is therefore not our proposed differentiation. [PTC announcement](https://www.ptc.com/en/news/2026/ptc-launches-ptc-orbit)
- Disassembly redesign also has prior art: LeanDfD analyses sequences/times and recommends changes; aPriori offers CAD manufacturing-cost analysis. Neither public page reviewed establishes the complete warranty-frequency-weighted, geometry-checked redesign workflow. That observation is limited to reviewed material. [LeanDfD](https://www.sciencedirect.com/science/article/pii/S2212827126005780), [aPriori](https://www.apriori.com/solutions/products/ap-design/)

### What remains unverified

Whether an existing PTC/Siemens/custom engineering installation already performs the same complete job; whether an OEM will share CAD and revision-linked claims; whether proposed changes improve economics after tooling and qualification; whether the same implementation can serve multiple customers without excessive consulting; and whether the reachable software revenue can support a large independent company.

The commercial entry would be one appliance family and one recurring expensive repair. A paid redesign study can establish data access and engineering usefulness. An annual product-line/engineering subscription is a hypothesis, not validated pricing. Broader potential includes other appliance and equipment families, but these require new constraints and integrations.

### Google buildathon demonstration

Use a small consented or self-created mechanical assembly, known repair instructions, explicit engineering constraints and clearly synthetic failure/cost records. Gemini extracts and relates textual instructions and records; a geometry/constraint solver checks candidate access/removal changes; deterministic calculations compare repair and manufacturing costs. Cloud deployment hosts review and analysis. Show one valid proposal and one rejected proposal. This demonstrates a bounded workflow, not OEM savings or production-ready automatic CAD design.

### Next verification gate

Ask an OEM service/design engineer to compare one real repair problem against its current PLM/quality workflow and a paid repairability assessment. Inspect whether the proposed output is missing and valuable. If the incumbent already produces it, or the customer primarily needs consultants rather than repeatable software, reject the standalone startup thesis. Do not recommend a broad build before this evidence.

## Candidates eliminated or held back

| Candidate | Evidence that weakened it | Decision |
|---|---|---|
| Billing/subscription test automation | Stripe test clocks already simulate lifecycle scenarios; TestChimp documents billing and entitlement tests | Reject generic version |
| Promotion stacking/margin protection | Talon.One explicitly offers stacking and abuse controls | Reject |
| Agent-memory lineage and invalidation | Lineleaf explicitly markets dependency lineage and invalidation; Auld describes deleting derived memories | Reject |
| Cross-provider agent transaction recovery | Temporal/Restate compensation, SagaLLM research and travel refund/change APIs cover much of the stack | Downgrade to discovery only; no independent product gap demonstrated |
| Agent-service acceptance/settlement | Jobs for AI Agents, dotsjobs and Taskin overlap acceptance and payment | Reject generic version; change-order lineage remains speculative |
| Dyehouse optimization | Existing colour/process monitoring and controls plus academic closed-loop work; narrower retrofit gap not established | Do not promote |
| Battery EPR evidence | CPCB records material/credit data; Recykal offers battery EPR and traceability | Do not promote |
| Supplier climate-disruption response | Quibas already describes supplier-site/order impacts and sourcing response | Reject per source scan |
| Treated-water exchange | NuWater and Project O overlap the matching/exchange job | Reject per source scan |
| C&I flexibility aggregation | Ingro and Tata Power/AutoGrid already address the category | Reject generic version |
| Heat-aware work scheduling | Close competitors; also overlaps an earlier idea already rejected by this user | Do not recycle it as new |
| Chemical process transfer/scale-up AI | gPROMS, Dynochem, Chemical.AI, ScaleChem, Atinary and Aizon cover much of the proposed workflow | Reject generic version |
| Generic cable-insertion robotics | Micropsi MIRAI and ABB already advertise cable insertion; Intrinsic challenge confirms active research, not an empty market | Reject generic version |
| Generic food shelf-life/formulation AI | Shelfion, AKA Studio, Proxy Foods and other vendors describe these jobs | Reject generic version |

Key supporting first-party links: [Stripe](https://stripe.com/blog/test-clocks-how-we-made-it-easier-to-test-stripe-billing-integrations), [TestChimp](https://testchimp.io/guides/flows/testing-subscriptions-billing/), [Talon.One](https://www.talon.one/product/offer-management-and-execution), [Lineleaf](https://lineleaf.dev/), [Auld](https://auld.app/), [Temporal](https://temporal.io/blog/who-needs-workflows-when-you-have-agents), [SagaLLM paper](https://www.vldb.org/pvldb/vol18/p4874-chang.pdf), [FercoScientific](https://www.fercoscientific.com/), [CPCB manual](https://eprbattery.cpcb.gov.in/upload/adminDoc/GuidanceManuals/Guidance%20Manual%20Recyclers.pdf), [Recykal](https://www.recykal.com/tech-led-epr), [Aizon tech transfer](https://connect.aizon.ai/hubfs/Aizon-Tech-Transfer-Solution-Brief.pdf), [Micropsi](https://www.micropsi-industries.com/blog/how-the-mirai-vision-system-works), [ABB](https://new.abb.com/news/detail/127283/wbstr-abbs-cobots-and-small-robots-bring-efficiency-and-precision-to-flexible-printed-circuits-cable-assembly), [Shelfion](https://www.shelfion.com/how-it-works), [AKA Studio](https://aka-food.com/formulation/).

These sources establish advertised capabilities or research results, not independently measured performance or market share. Research prototypes, vendor marketing and deployed commercial offerings are different evidence types.

## Complete supporting notes

- [Agent infrastructure, including adversarial second pass](verified-new-agent-infrastructure.md)
- [Energy and industrial screen](verified-new-energy-industrial.md)
- [Initial cross-domain hypotheses](verified-new-crossdomain.md): preliminary survivor labels are superseded by this synthesis.
- [Repair economics competitive check](verified-repair-economics.md)
- [Process transfer check](verified-process-transfer.md)

No interviews, competitor product trials, customer commitments, paid orders or independent technical benchmarks were completed. No outreach was performed.
