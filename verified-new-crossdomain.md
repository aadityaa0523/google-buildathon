# Two startup hypotheses after competitor checks (India)

Research checked 13 November 2026. These are hypotheses, not claims of uniqueness. The user asked to avoid several already-rejected categories; those are excluded.

## 1. Closed-loop dyehouse batch control for Indian wet-process textile mills — survivor

**The job:** A dyehouse process engineer has to get each customer lot to the approved shade while holding water, steam, chemical use, and re-dye/rework down. The costly work is not recording a recipe; it is translating a lab-approved target to different machines, liquor ratios, fabric lots, incoming-water conditions, and operator execution, then correcting the batch before the whole lot is lost.

**Product hypothesis:** Retrofit industrial controls and a process model that ingests recipe/lot data, machine temperature and flow traces, water hardness/conductivity, and spectrophotometer readings; predicts shade drift and recommends or safely actuates correction dosing/rinsing/stop decisions. Start in one repeatable segment (e.g. polyester piece-dyeing in Surat), with an operator approval step. Measure first-pass shade yield, re-dye rate, water/steam per kg, and batch cycle time. This is an operating intervention at the machine, not another job-card/ERP dashboard.

**Why there is a buyer:** NITI Aayog's sector analysis says textile finishing (including dyeing, drying, washing) consumes about 43% of sector energy, with 73% of that met by coal, and calls out wastewater/chemical pollution. A Government of India dyes compendium reports dyeing water use varying 36–176 L/kg (average 106 L/kg). Those make measurable savings economically material; mills/process houses can buy against reduced rework, steam, water, and chemical consumption. The pilot should be priced as installation + annual controls software/service, with a verified savings share option.

**Competitive overlap checked:** Centrio explicitly sells dyehouse ERP with batch planning, recipes, chemical consumption, production tracking, QC and reprocessing: that is an adjacent incumbent and makes a generic workflow product a no-go. Indian colour vendors such as Kothari Colorist sell recipe prediction and lot shade sorting; Scientific Software sells colour analysis/QC and online dyebath concentration monitoring. These products confirm the technical/operational terrain is occupied. The narrower opening to test is cross-machine, in-process closed-loop control and energy/water optimization tied to actual batch outcomes; do not assert that no incumbent offers it. Before building, interview/install alongside two process houses and compare with their current machine controls and CCM vendor capabilities.

**Scale path:** Prove economics in one cluster and machine family, then repeat by machine/controller integrations across Surat, Tiruppur, and other wet-processing clusters. A cross-plant process/outcome dataset can improve recipes and controls, but only with permission and careful separation of customer formulations.

**Hardest constraint:** Reliable sensor/PLC integration and trustworthy process labels across old heterogeneous machines; a bad correction can ruin a whole lot. Must demonstrate safe bounded control and independently verify savings, not sell AI predictions alone. Adoption also depends on dye-master trust and compatibility with installed CCM systems.

## 2. Battery take-back chain-of-custody and material reconciliation for Indian battery producers — conditional survivor

**The job:** Producer EPR teams must reconcile batteries placed on market with collection, recycler receipts, recycled output, and EPR certificates across producers, collectors, and recyclers. This is a physical mass-balance and evidence problem: batteries are heterogeneous, mixed chemistry/condition, and often move through fragmented collection channels. A producer can face a compliance gap even when the data is spread across counterparties.

**Product hypothesis:** A transaction-level evidence and reconciliation rail for producer responsibility organizations and battery producers: register collection events with weight/chemistry/serial or batch evidence, reconcile recycler weighbridge and recovered-material records against certificates, detect duplicate/implausible claims, and export validated returns to CPCB portal. It should integrate with collection and recycler weighbridge operations; a standalone filing reminder tool is not the product.

**Why there is a buyer:** CPCB's official Battery EPR portal says the rules apply to all battery types and producers carry EPR collection/recycling obligations; it describes traceability/transparency as a portal objective. CPCB's recycler manual specifically calls for recording procurement/recycling data, recovered-material sales, EPR-credit generation/transfers, and quarterly returns. Producer or PRO pays for auditable reconciliation, lower manual exception work, and reduced risk of unsupported credits; potentially per ton reconciled plus enterprise integration.

**Competitive overlap checked:** CPCB already operates the statutory registration/returns/credit portal, so a duplicate compliance portal is dead on arrival. YANTI markets battery lifecycle intelligence across warranty/service/fleet/circularity; MOBIUS+ markets a battery lifecycle API unifying manufacturer, fleet, service, and recycler data; those overlap the broad “battery passport/lifecycle platform” framing. This idea survives only as a narrowly defined physical EPR mass-balance and evidence layer integrated with the government portal and counterparties, not as a battery passport or general lifecycle dashboard. Validate existing PRO/recycler software before treating the seam as open.

**Scale path:** Begin with one PRO/recycler route and a battery segment, reconcile real weights/credits, then sell to multiple obligated producers and recyclers. As a trusted rail, extend to transaction assurance and recovered-material provenance; never create or trade EPR credits itself.

**Hardest constraint:** Counterparty adoption and truthfulness of physical weights/chemistry; a polished database cannot fix unmeasured or fraudulent chain-of-custody. CPCB portal changes and legal interpretation also create integration/support burden. The regulatory demand exists, but willingness to pay for a separate reconciliation layer remains unproven.

## Ideas rejected after overlap check

- Generic repair-shop workflow / appliance service dispatch: SaralFix, Kiwikit, Tazk ReCare and Servsy already advertise close India-fit offerings. Right-to-repair information access is also a government portal use case.
- EV battery health passport / diagnostics: ev.care and The Honest EV advertise battery passport/diagnostics, while YANTI and MOBIUS+ cover broader battery lifecycle intelligence. Too close to existing propositions.
- Dyehouse ERP, recipe management, or shade prediction alone: Centrio and established colour-management vendors already sell these. The proposed textile hypothesis is limited to feedback/control at the process machine.
- Engineering change / PLM or generic BIS/QCO tracker: large PLM vendors and certification consultancies already operate here; a thin regulatory alert layer is not a defensible startup.

## Sources (primary product/regulatory sources; accessed 2026-11-13)

- NITI Aayog, *Scenarios Towards Viksit Bharat and Net Zero — Industry*: https://www.niti.gov.in/node/2168
- Government of India, *Textile Dyes Compendium*: https://www.dbtindia.gov.in/sites/default/files/Textile_Dyes_Compendium-Final.pdf
- Centrio dyeing/printing ERP product: https://centrio.in/pages/erp-software-for-dyeing-and-printing-units
- Kothari Colorist: https://www.kothariinfotech.com/kothari-colorist.html
- Scientific Software: https://ssccltd.in/
- CPCB Battery EPR portal: https://eprbattery.cpcb.gov.in/grid
- CPCB recycler guidance manual: https://eprbattery.cpcb.gov.in/upload/adminDoc/GuidanceManuals/Guidance%20Manual%20Recyclers.pdf
- YANTI battery lifecycle product: https://www.yanti.co.in/
- MOBIUS+ battery lifecycle API product: https://mobius-plus.com/
- ev.care battery passport product: https://ev.care/service/battery-passport
- The Honest EV product: https://www.thehonestev.com/
- Right to Repair India: https://righttorepairindia.gov.in/about
- SaralFix: https://saraltechies.com/saralfix
- Kiwikit: https://www.kiwikit.in/repair-shop-software
- Servsy: https://servsy.in/crm

## Confidence / open checks

The textile control-loop is the stronger candidate; the EPR evidence rail is conditional and could collapse into CPCB portal functionality or a PRO's existing system. Website product claims establish direct competitor scope, not market share, customer outcomes, or absence of other vendors. Neither idea should be presented as unique without buyer interviews and a hands-on incumbent review.
