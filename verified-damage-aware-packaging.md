# Damage-aware protective packaging redesign: verification note

**Checked:** 2026-11-13. **Purpose:** assess whether the proposed idea has a defensible opening beyond cartonization, right-sizing, packaging-specification management, and CAE simulation.

## Verdict

There is a real engineering problem, but the broad idea is already substantially served. Amazon describes a learned package-type recommender that explicitly optimizes packaging cost against damage cost; in its own large-scale deployment it reported 24% fewer damaged shipments and 5% lower shipping costs. Paccurate says its current control system optimizes packing rules and packaging choices, can analyze historical shipments, and lets customers specify protection requirements by SKU/class. Packsize sells custom packaging design that aligns product dimensions, protection requirements, and order variability. Ansys sells packaging drop/crush/transport simulation with product and package geometry/material models. A pitch saying “AI uses damage data and CAD to redesign protective packaging” risks combining these existing capabilities under a new label.

The narrower, not-yet-verified opening is a **closed-loop, SKU-level engineering workflow** that joins *observed damage mode + lane/handling exposure + package design revision + measured test outcome + delivered claim/return cost*, then recommends a costed geometry/material change and tracks whether pilot results improved. The reviewed public product descriptions do not establish that any one named vendor provides this complete cross-system loop. That absence in public descriptions is not proof of absence, nor proof of demand. Treat this as a hypothesis to validate with packaging engineers and damage/claims owners; do not claim uniqueness or validated demand.

**Recommendation:** conditional, not a clean greenfield SaaS idea. Proceed only if the team can identify a buyer with siloed claims and package-spec/test data and a repeatable product family where the economics justify measured redesign. Otherwise this likely becomes a packaging-engineering consultancy/integration project, and the stronger software products already cover adjacent steps.

## Problem and spending evidence

- Damage is financially actionable: UPS claim workflows request item value/invoice and damage documentation; its terms require original packaging to be available for inspection in damage claims. This shows claim value and packaging are captured in the resolution process, but does not quantify total industry loss. [UPS claims requirements](https://www.ups.com/us/en/support/file-a-claim), [UPS U.S. terms](https://wwwapps.ups.com/assets/resources/webcontent/en_US/terms_service_us.pdf)
- I found no trustworthy public primary source in this pass that quantifies a broad annual addressable-spend number for parcel product damage. Do not repeat unsourced market-loss statistics. A commercial case must use a prospective customer's own damage/return/repair, replacement, freight, claims-recovery, packaging, and test-lab costs.
- ISTA's public project page describes a multi-phase effort to quantify transit-damage monetary impact and typical levels by commodity/mode, and notes progress was slow while assembling a sufficiently broad, de-identified base. This supports that comparable data aggregation is difficult; it does not establish buyer demand for this product. [ISTA transit damage research project](https://ista.org/advocate_research_value_deli.php)

## Closest products and overlap

| Product/source | What it publicly says it does | Implication |
|---|---|---|
| Amazon research | Recommends package type by product, balancing packaging and damage costs; reports deployment result on hundreds of thousands of packages. [Amazon Science](https://www.amazon.science/blog/how-to-compute-the-optimal-way-to-package-amazon-products) | Directly defeats the claim that damage-aware package selection is novel. It focuses on choosing package types, not publicly documented parametric protective geometry redesign. |
| Paccurate | Cartonization/packing control, historical-order simulation for package lineup, and SKU/product-class protection rules. [Paccurate product](https://paccurate.co/), [Paccurate on-demand cartonization docs](https://docs.paccurate.io/docs/on-demand-cartonization) | Strong direct overlap in data-driven packing decisions and protective requirements; public pages do not prove it performs CAD-level cushioning geometry redesign from observed failure modes. |
| Packsize | Right-sized/on-demand packaging software and custom packaging design for product dimensions, protection requirements, and operational realities. [PackNet](https://www.packsize.com/software), [custom packaging design](https://www.packsize.com/solutions/custom-packaging-design) | Overlap in design and protection. Not safe to claim “right-sizing ignores damage.” Narrow opening must be measured failure-mode-to-engineering-revision traceability. |
| Specright / ISTA PackSight | Packaging specification management and an online workflow to select, collect, and analyze ISTA tests. [Specright PackSight](https://www.specright.com/ista-packsight/) | Overlap in specs/test workflow; reviewed page does not establish automatic redesign recommendations. |
| Ansys LS-DYNA | Simulation-led packaging engineering: drop, crush, transport handling, material models including corrugate, foam, paper, plastic, plus optimization. [Ansys packaging simulation overview](https://innovationspace.ansys.com/product/innovating-consumer-packaging-with-ansys-ls-dyna/), [drop-test demo](https://www.ansys.com/resource-center/demo/drop-test-demo) | Exact engineering capability exists. Likely expert-heavy CAE workflow; product opportunity would need to reduce data/model setup and connect field failures to simulation/validation, not claim the solver capability. |
| ISTA testing | Test protocols and customer-defined product damage/pass criteria; product/market/distribution context matters. [ISTA guidance](https://ista.org/docs/2020_ISTA_Guidelines.pdf) | A model cannot independently label “safe”; customer-defined damage thresholds and physical validation remain required. |

## Candidate buyer and business shape

First buyer to test: **packaging engineering or product reliability lead at a shipper/manufacturer with high damage cost, repeat shipments, multiple package variants, and centralized claims/test data**. The economic approver may be operations, quality, or supply-chain finance. A parcel carrier may supply exposure data, but the shipper controls product fragility, acceptable damage, package specs, and redesign decisions. A test lab/packaging converter could be a channel, though that creates potential services dependence.

A software business would need a repeatable onboarding path (ERP/WMS/claims + CAD/spec + test data), versioned package recommendations and ROI tracking across many SKUs/sites, plus a subscription or per-SKU/facility pricing model. If every deployment needs manual claims normalization, custom CAD cleanup, FEA modeling, packaging material characterization, and lab testing, revenue is likely services-led. High switching costs and proprietary cross-customer damage data are possible, but not established; sharing claims/CAD is a sensitive-data barrier.

## Buildathon-sized Google demo

Use a small synthetic dataset for 3 fragile products, 3 package revisions, and 2 lanes. Ingest example CSVs for shipped units, damage/claim mode, observed handling/lane, package BOM/cost, and test outcome. Show (1) ranked SKU/package hotspots and estimated damage cost, (2) a transparent recommendation card proposing one geometry/material change with estimated material cost and rationale, (3) a test matrix based on the selected ISTA-like drop/compression/vibration conditions, and (4) a before/after pilot dashboard with confidence/limitations. Google stack could be a simple web app with Cloud Run and BigQuery; Gemini can turn structured findings into a readable engineering brief, while deterministic rules/calculations own the scores and estimates.

Do **not** present generated geometry or simulated pass/fail as validated engineering output. Clearly label the recommendation as a candidate requiring packaging engineer review and physical transit testing. A compelling demo proves the workflow and audit trail, not predictive accuracy or customer demand.

## Open questions before backing the idea

1. Can a target shipper export damage/claim records keyed to SKU, lane, and package revision, including enough reason-code quality to distinguish packaging failure from carrier/product/manufacturing causes?
2. Do current providers already close this loop through private integrations, services, or customer-specific implementations (not visible in public product pages)?
3. Is there enough volume/value in a narrow vertical (e.g. appliances, glass, electronics) to pay for reliable CAD/spec integration and physical testing?
4. Can package changes be evaluated quickly enough to make a recurring product, rather than episodic engineering engagements?

## Sources

All sources above are primary sources (vendor documentation/product pages, ISTA materials, carrier terms, or Amazon's own research publication). Vendor efficacy figures are vendor-reported and should not be treated as independently verified.
