# As-measured nonconforming-part repair planning: verification note

**Reader decision:** retain only the narrow repair-versus-replacement optimization concept as a research candidate, below the previous warranty-informed redesign candidate. Do not interpret this note as a recommendation to build, a uniqueness finding, or validated demand. Generic repair instructions, adaptive repair routing, and machining correction were rejected.

**Checked:** 2026-11-13. **Question:** Is a startup that turns as-measured defect geometry, remaining tolerances, and recertification requirements into repair/rework instructions sufficiently unserved to recommend?

## Verdict: do not recommend as currently framed

The broad manufacturing nonconformance workflow is established in enterprise QMS/MES: capture defect, analyze/triage, route for approval, choose rework/repair/scrap/use-as-is, and preserve evidence. Siemens Opcenter explicitly offers event and nonconformance management with risk triage, failure analysis, quarantine and final disposition; NX CAM on-machine probing already uses live measurement to adjust machining and rework, including measured geometry against the CAD design and closed-loop correction. Oracle Quality documents rework/repair disposition workflows. So “AI writes repair instructions for defective parts” would collide with existing QMS and CAM functions.

A genuinely narrow seam remains plausible: **for a specific class of expensive, machinable components, compute and verify a safe salvage plan from a full-field as-measured surface/defect map, remaining stock/tolerance budget, material/process limits, and the authorized repair standard, then export a traceable machine-ready rework plan and recertification evidence package.** Sources reviewed do not show a general commercial product that autonomously computes this entire plan. But this is an inference from public product descriptions, not proof no private or vertical solution exists. It is also a technically and safety-critical problem with process qualification as a major barrier. Do not pitch a general-purpose AI rework copilot or suggest engineering authorization can be automated.

This narrowly resembles engineered repair workflows already practiced in specialist sectors, and underlying digital capabilities exist. A research paper documents scan-to-repair-volume generation for laser directed-energy-deposition repair of a die insert using Hexagon scanning/PC-DMIS, Boolean geometry and machine-specific toolpaths. That makes the seam a **packaged vertical workflow opportunity**, not novel underlying science. [Journal of Materials Processing Technology paper](https://doi.org/10.1016/j.jmatprotec.2026.119301)

## Closest existing capabilities

| Source | Existing capability | What remains unestablished |
|---|---|---|
| Siemens Opcenter | Nonconformance capture, risk triage, failure analysis, quarantine, approved dispositions such as repair/rework/scrap/use-as-is, traceability. [Siemens overview](https://www.siemens.com/et-ee/technology/nonconformance-management/) | Public overview does not claim geometric feasibility computation or machine-ready salvage plans from scan data. |
| Siemens NX CAM probing | Measures before/during/after machining; integrates CMM programming, PMI, as-built results vs 3D design, adaptive control and cut-measure-cut correction. [NX probing](https://www.siemens.com/en-us/products/nx-manufacturing/cam-software/on-machine-probing/), [NX 2606 release](https://blogs.sw.siemens.com/nx-manufacturing/whats-new-in-nx-for-manufacturing-2606-june-2026/) | This is direct overlap for measured-geometry machining correction. The distinction is nonconforming-part salvage across repair process qualification and disposition, rather than correcting in-process variation. |
| Oracle Quality | Formal nonconformance review and approved rework/repair disposition execution with closure. [Oracle Quality guide](https://docs.oracle.com/cd/B40089_06/current/acrobat/120qaig.pdf) | Workflow execution, not shown as generating geometry-aware repair instructions. |
| Hexagon + specialist repair paper | A demonstrated scan/point-cloud-to-repair-volume workflow for laser DED repair of a die insert, with metrology and Boolean operations. [Research paper](https://doi.org/10.1016/j.jmatprotec.2026.119301) | Demonstration is a custom technical chain, not evidence of repeatable SaaS/product demand. |
| Siemens SINUMERIK probing | CNC measuring cycles can compare measured values to setpoints and initiate compensation. [Siemens measuring cycle manual](https://support.industry.siemens.com/cs/attachments/109822991/ONE_meas_cycles_progr_man_0723_en-US.pdf) | Compensation for process variation is not necessarily an approved repair disposition for a finished nonconforming part. |

## Buyer and business reality

Potential first buyer: repair engineering / MRB lead at an aerospace, energy, tooling, or heavy-equipment manufacturer where scrapping a high-value machined component is expensive and repair is already allowed by controlled procedures. Quality authority and the OEM/customer approve the disposition; the product must respect that authorization and produce evidence rather than make a final safety decision.

A scalable product probably needs to start in one repair process and material/component family (for example, die inserts with a qualified DED repair procedure), integrate a specific scanner/metrology format and CAM/DED system, and map against a controlled repair standard. A horizontal SaaS would face divergent materials, damage modes, tolerances, process qualification, customer approvals, and liability. If every job requires materials/FEA/CAM expertise and custom process qualification, it is a high-value engineering service with software aids rather than a software-first business.

## Bounded demo if exploring the seam

Build a synthetic demo around one non-safety-critical machined plate with an oversize bore or shallow surface defect. Input nominal CAD, a small measured point cloud/deviation map, material-removal limits, tolerance table, and a fictional approved work instruction. The app should calculate residual stock/tolerance feasibility, reject unsafe/out-of-envelope cases, show an engineer-reviewable candidate toolpath envelope, and produce a before/after inspection checklist plus provenance/evidence report. Keep geometry calculations deterministic; use Gemini only to draft an explanation from computed values. Label every output “engineering review required”; do not claim it computes a qualified repair plan or certifies part fitness.

## Evidence limits

### Further research overlap found by the parent

Even multi-route optimization is not new science:
- [Reliability and cost optimization for remanufacturing process planning (2016)](https://www.sciencedirect.com/science/article/pii/S0959652615016777) models reliability and machine/tool costs to select process plans.
- [Optimizing quality and cost in remanufacturing under uncertainty (2024)](https://link.springer.com/article/10.1007/s11740-024-01314-x) generates cost/quality tradeoffs and assigns available cores to orders. The authors report a real-world automation-industry application and provide code/data. This is technical feasibility evidence, not proof that our proposed startup has customers.
- [Virtual-twin regeneration decision support (2022)](https://www.tandfonline.com/doi/full/10.1080/00207543.2022.2051089) describes selecting alternative repair paths using functional condition and scheduling. The search-indexed abstract/excerpts were accessible; direct full-page access returned 403 in the parent's check.

Consequently, the defensible thesis is commercializing a tightly scoped, geometry-grounded decision tool for a buyer whose present tools do not perform the comparison economically. No claim of algorithmic invention is justified. Commercial availability in specialist integrations remains unresolved.

### Concrete product hypothesis and falsification test

Start with one family of non-safety-critical industrial tooling, using existing engineer-qualified repair methods. Inputs: measured condition, nominal geometry, material and prior repair history, controlled allowable repair envelope, inspection requirements, replacement quote and delivery date, and process quotes/capacity. Compute which configured routes are admissible; show the binding constraint and total prospective repair/testing cost versus replacement. A surface scan cannot establish internal cracks, metallurgical condition, or fatigue life; missing necessary evidence must block a positive feasibility result.

The buyer hypothesis is a tooling or repair-engineering manager. The commercial hypothesis is subscription or per-assessment pricing after a paid retrospective evaluation. Expansion to more component families is a possibility, not a measured TAM. Diverse qualification rules and manual modeling may prevent repeatable software economics.

Before backing it, replay 20 closed cases with a repair team: include repaired, scrapped and ambiguous cases; compare against its current engineering/CAM workflow. Require identification of unsafe/ineligible routes, evidence for all critical constraints, measurable engineering-time or economic improvement, and willingness to pay. Do not infer demand from academic demonstrations. No interviews or paid pilots have been conducted.

For a Buildathon prototype, use one explicitly synthetic geometry and engineer-configured rule set, two allowed recovery routes and replacement. Gemini can extract candidate fields with source references for confirmation; a geometric/constraint solver performs feasibility and cost calculations. Host on Google Cloud. Show both a feasible case and a case rejected for insufficient remaining material. The event asks for a new AI product using Google AI and deployed on Google Cloud: [official event](https://startupbuildathon.com/). Image interpretation capability: [Google documentation](https://aistudio.google.com/docs/image-understanding). This is proposed architecture, not an implemented or physically qualified system.

No reliable broad primary-source spend figure was located for this niche. The business case must be built from a target repair shop's own scrap/repair cost, cycle time, approval burden, and recertification records. Public sources support that the workflows and tooling exist; they do not validate the proposed product's demand or a standalone market gap. The source set reviewed was intentionally bounded and focused on Siemens/Oracle/Hexagon; it is not an exhaustive patent or vendor search.

## Second-pass overlap check (stronger than the initial search)

The parent identified additional direct overlaps, which materially narrow the opportunity:

- **MRB Disposition Generator** reports ERP-fed defect classification, precedent search, authority-limit checks, and generation of controlled rework instructions; for novel defects, it drafts a guided disposition from verified reference data with engineer approval. This is an individual practitioner’s production deployment, not a broad vendor product, but it shows that paperwork/knowledge synthesis is already implemented. [MRB Disposition Generator](https://mattwhitt.com/ai-work/mrb-disposition/)
- **Aegis FactoryLogix MRO** explicitly builds adaptive repair routes as diagnosis reveals conditions, compares as-built/as-returned configuration, manages MRB dispositions/rework loops, and updates guided repair instructions with contextual 3D CAD. This is a strong commercial competitor for variable repair workflows, genealogy, and authorization. It may not calculate geometric salvage feasibility or optimize material-removal/repair routes from a full-field scan, but the high-level adaptive-repair claim is occupied. [Aegis MRO](https://www.aiscorp.com/solutions/mro)
- **CNC Probing AutoFinish** is described by the parent as autonomous measure-correct-finish; its page was not retrievable in this browsing pass, so treat details as parent-supplied rather than independently checked here. [AutoFinish](https://www.cncprobing.com/en/autofinish.html)
- Siemens NX also publicly describes closed-loop probing and cut-measure-cut correction, confirming that routine offset correction is an established CAM function. [NX probing](https://www.siemens.com/en-us/products/nx-manufacturing/cam-software/on-machine-probing/)

Therefore, even the refined candidate should **not be recommended yet**. Only the physical-route optimization seam remains unverified: compare multiple feasible repair methods (e.g. machine-to-size, weld/DED restore then machine, coat/plate then finish, accept with concession, scrap) using the actual scan, residual tolerance/material, qualified procedures, expected yield, cost, lead time, and approval constraints. The reviewed sources don't show a commercial solver for this exact multi-route economic decision. That is a narrow inference, not a validated market gap; a brief patent/vendor search and interviews with one repair engineering/MRB team would be needed before recommendation. If pursued for a demo, use a single non-safety-critical component, explicitly configured allowable routes and synthetic costs; the tool should only rank routes that a qualified engineer has approved as technically admissible.
