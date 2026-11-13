# Accelerator startup mechanisms adaptable to an India Google AI/Cloud demo

**Review status:** Preliminary source research. [The final synthesis](startup-programs-google-buildathon.md) adds direct vGIS competition, relevant Indian tender text, Scale/Toloka and public dataset substitutes. The user's confirmed robotics/AI researcher access moves task-specific evaluation/data work to first discovery priority. Android support alone is not differentiation; full phone-based robotic evaluation must not be implied without action/state data and actual trials.

**Prepared:** 13 November 2026  
**Scope:** Six accelerator-backed products whose underlying business mechanisms may transfer to India. This is an opportunity screen, not evidence of demand: India buyer pain, sales access, prices, and incumbent coverage need validation. Cohort and product descriptions below are attributed to the startups’ official accelerator directories or first-party product pages. No claims of market absence or traction are inferred.

## Shortlist and ranking

| Rank | Startup / cohort | Mechanism worth adapting | India wedge and likely buyer | Demo fit |
|---|---|---|---|---|
| 1 | [sizeless — YC Summer 2023](https://www.ycombinator.com/companies/sizeless) | Turn field capture made during work into a structured, auditable record used for QA and billing, removing a second survey visit and shortening the gap to invoice. | A civil/pipeline contractor or private campus utility works contractor that must submit evidence and quantities before a trench is closed; sell on faster accepted documentation and fewer return visits. | Strong: Android capture → evidence QA → reviewer decision → invoice-ready work package. Keep measurements human-verified in the demo. |
| 2 | [Kanopy — YC Fall 2026](https://www.ycombinator.com/companies/kanopy) | Convert routine corridor video into a prioritized asset-risk map, then verify that dispatched maintenance actually resolved the issue. | A power distribution contractor or private renewable/industrial network operator; initial outcome could be fewer manual patrols and documented clearance work. | Strong CV demo, weaker access: sample imagery can show risk map and before/after verification; utility procurement/data access are the hard parts. |
| 3 | [Human Archive — YC Winter 2026](https://www.ycombinator.com/companies/human-archive) | Build a paid field network that collects structured, consented physical-world data with quality control and delivery specifications. | A robotics team needing repeatable evaluation data from Indian work settings; a narrow data collection/evaluation package could be a testable pilot. | High team fit (Android, embedded, CV, agent evaluation), but YC says Human Archive already has India operations; avoid cloning its general data-lab offer. |
| 4 | [Tenyks — YC Summer 2021](https://www.ycombinator.com/companies/tenyks) | Make existing video operationally queryable and tie observations to a concrete decision, rather than sell camera hardware. | Restaurant/franchise operations teams, but a focused local buyer and distinct paid outcome must be found. | Easy mock demo, weaker differentiation: the company already sells restaurant video operations intelligence. |
| 5 | [Cerrion — YC Summer 2022](https://www.ycombinator.com/companies/cerrion) | Learn normal production from installed cameras, detect a costly deviation, and connect detection to a preventive action and incident evidence. | A line owner with recurring stoppages, but this is a crowded and familiar industrial CV direction; pursue only with a sharply bounded process and a willing plant. | Excellent CV prototype, difficult production access and safety/PLC validation. |
| 6 | [Dream — YC Summer 2026](https://www.ycombinator.com/companies/dream) | Create a continuous condition history as valuable equipment changes hands, then attribute new damage at intake/return. | Equipment rental, fleet, or dealership operators. The mechanism is real, but India already has adjacent vehicle inspection products; not a strong whitespace thesis. | Easy before/after photo demo; avoid generic “AI vehicle inspection.” |

## 1. Recommended: trench-work evidence that unlocks QA and billing

### What the reference company does

YC lists sizeless in its Summer 2023 batch. The company describes guided smartphone video of an open trench being converted into a 3D record and CAD/GIS outputs. Its launch post says the same record includes pipe/component recognition and billable quantities; its current product page describes faster documentation and contractor invoicing as customer outcomes. The current field app specifically targets iPhone Pro, so Android capability is an adaptation to validate rather than an assumed parity feature. [YC profile and launch](https://www.ycombinator.com/companies/sizeless), [sizeless product](https://sizeless.co/product/), [FAQ](https://sizeless.co/en/faq)

### India product thesis

Build a **work-completion evidence packet** for underground water, fiber, or power repair: the crew captures a short guided video while the trench is open; the app checks required views and site identity; a reviewer sees a location/time-stamped sequence, extracted visible components, voice notes, annotated stills, and a checklist; the contractor exports an accepted work package tied to its bill item. The initial promise is “fewer return visits and a complete QA/billing packet the same day,” not survey-grade digital twins or automatic statutory acceptance.

This shifts value from “AI makes a 3D model” to a coordination asset: a shared record captured before the evidence disappears under backfill, which can let the contractor and owner resolve missing-work disputes while the site is still accessible. The contractor is the first paying user because delayed documentation can delay invoicing; the owner/utility reviewer is the second user who accepts, rejects, or asks for recapture. Treat this payment-delay hypothesis as unverified until interviews and a pilot prove it.

### Two-day demo

1. Android app: choose a work order, capture a guided 20–40 second walkaround and required close-ups, record a short note, and retain capture time/location plus original media.
2. Processing: Gemini proposes labels for visible pipe/valve/connection types and transcribes or summarizes the note. A deterministic capture checklist flags missing views, blur, or absent work-order markers. Do not present model guesses as certified dimensions.
3. Reviewer web view: scrub video, inspect timestamped frames and labels, compare against a small mock scope of work, request recapture or accept, and produce a PDF/CSV evidence packet with the linked bill item.
4. Demo with 2–3 staged trenches (or tabletop pipe mockups) and make one capture deliberately incomplete to show the value of capture QA and review, not just a VLM summary.

### Hardest validation and competition

- **Critical buyer test:** Will a contractor pay for the packet because it reduces return visits or gets an invoice accepted sooner? Ask a contractor and the owner-side engineer to review a real completed job, compare the current documentation path, identify who controls acceptance, and name a paid pilot trigger.
- **Technical test:** Does ordinary Android footage consistently capture the visual evidence reviewers need in cramped, muddy, low-light, or crowded trenches? Test low-cost devices and weak connectivity; upload must resume and preserve originals.
- **Trust / liability test:** Which measurements and records can be accepted from phone capture, and which still require a licensed surveyor or existing GIS workflow? Keep a human sign-off and explicit provenance. Do not claim legal compliance from the prototype.
- **Adjacent India offerings:** Existing GIS/field survey and drone inspection providers are relevant alternatives; Infosys describes drone imagery and AI for vegetation management, while Vidrona’s cited power-sector solution describes drone inspection of grid assets. These are adjacent, not evidence that trench documentation is served or unserved. [Infosys utility vegetation solution](https://www.infosys.com/services/data-analytics/insights/vegetation-management-solution.html), [India power-sector case-study PDF](https://sarepenergy.net/wp-content/uploads/2023/07/20230217_Revised-Cover-Drone-Applications-for-Power-Sector_Whitepaper_FINAL-Print.pdf)

## 2. Runner-up: corridor inspection through to verified maintenance

YC lists Kanopy in Fall 2026. Its profile says the company converts ordinary video from drone, vehicle, or phone into a 3D infrastructure model, measures vegetation clearance, identifies hazards/asset condition, and supports maintenance prioritization and verification. [YC profile and launch](https://www.ycombinator.com/companies/kanopy)

An India adaptation could focus on a bounded corridor and paid action loop: capture line imagery, create a ranked list of clearance risks, dispatch a vegetation crew, then recapture only the flagged spans and issue a before/after completion record. The buyer is the utility or its maintenance contractor. Test willingness to pay for one route’s inspection and verified clearance report before expanding to a broad grid “operating layer.”

**Demo:** mark a small set of spans in sample video; show flagged tree/asset cases with map locations, urgency, work assignment, and follow-up evidence. A human confirms every risk and resolution. Google Gemini video can summarize and point to timestamps, while actual clearance estimation requires calibrated geometry / CV and ground truth; a language model alone should not decide safe clearance. India already has adjacent drone/CV capacity (see above), so differentiation must come from lower-cost repeat capture, accepted inspection records, or close-loop contractor verification. The hardest validation is obtaining utility footage and proving that the output changes a maintenance decision.

## 3. Conditional / adjacent: paid physical-world data collection

Human Archive’s YC Winter 2026 profile describes a physical-AI data lab using cameras and sensors to collect multimodal datasets and says it has offices in India. Its launch materials describe field capture hardware, QA and annotation pipelines, and partner access to real work environments. [YC profile and company launch](https://www.ycombinator.com/companies/human-archive)

This maps well to computer vision, Android, embedded systems, and agent evaluation. A differentiated small experiment could be a **task-specific evaluation set for a single physical agent** (for example, shelf restocking or a maintenance inspection) where multiple Indian sites record the same task under controlled variation; the deliverable is an evaluation protocol, labeled failure cases, and benchmark report, not generic video hours. A robotics/AI lab pays for task coverage and reliable labels. The main risks are already-active direct competition, worker consent/privacy, site access, operational cost, and finding a buyer before collecting data. Do not start with custom wearable hardware; test using phones and an existing partner site first.

## Additional references screened

### Tenyks (YC S21): operational restaurant video

Tenyks’s YC profile describes visual intelligence over CCTV, drone, and satellite video, initially focused on QSR customer flow, kitchen efficiency, staffing, and service quality. Its current site describes analytics from existing restaurant cameras. [YC profile](https://www.ycombinator.com/companies/tenyks), [company product](https://www.tenyks.ai/)

The mechanism—reusing existing cameras to improve a measurable operating metric—is sound. It is not a top India opportunity from this screen: the current product already targets restaurants and reports operational ROI; an India version needs a narrower unmet measure, local deployment advantage, or channel to win. A demo that merely summarizes CCTV would look like an AI wrapper.

### Cerrion (YC S22): event detection connected to prevention

Cerrion’s YC profile describes learning the normal appearance of a line from standard cameras and detecting production problems. Its product site describes alerts and, where integrated, preventive actions such as stopping a machine section or rejecting a product; the site also publishes customer examples. [YC profile](https://www.ycombinator.com/companies/cerrion), [product](https://www.cerrion.com/), [customer example](https://www.cerrion.com/customers/stoelzle)

The useful mechanism is closed-loop economics: the camera event is valuable when it prevents waste/downtime, not when it creates another dashboard. It is deprioritized because factory video analytics is familiar, plant access is difficult, and real control actions require safety and integration work. A team should test a single non-safety-critical bottleneck with a plant sponsor before prototyping.

### Dream (YC S26): continuity of asset condition

YC lists Dream in Summer 2026 and describes automatic multi-angle asset capture, identification, reconstruction of a condition record, and detection of new damage at return/intake. [YC profile](https://www.ycombinator.com/companies/dream)

The reusable mechanism is a condition history that follows an asset across custody changes, reducing disputes over who caused damage. However, India has clear adjacent products: Inspektlabs describes video-based vehicle inspections for insurers and sharing-economy fleets, and Indian vendors Lagaam and AutoSpect describe AI damage inspection. [Inspektlabs](https://inspektlabs.com/), [Lagaam](https://lagaam.in/products/ai-vehicle-inspection), [AutoSpect](https://www.autospect.ai/). This supports a crowded-adjacency warning, not a claim that all subsegments are saturated.

## Google AI and Cloud implementation map

Use Google products for media capture, asynchronous processing, and demo deployment; keep domain-critical dimensions and acceptance decisions grounded in deterministic checks and human review.

| Layer | Suggested Google implementation | Why / limitation |
|---|---|---|
| Android capture | Kotlin + CameraX; local queue and upload retry | CameraX is the recommended camera library path for Android app capture. [Android camera library guide](https://developer.android.com/media/camera/choose-camera-library) |
| Media storage | Firebase Authentication + Cloud Storage for Firebase | Android SDK supports media file uploads and resumable transfers; security rules should require authentication. [Firebase Android upload docs](https://firebase.google.com/docs/storage/android/upload-files) |
| AI assistance | Gemini video/image input for timestamped event notes, component labels, missing-view suggestions, and bilingual note summary | Gemini API supports video inputs and timestamp references; its default video mode samples at 1 FPS, so brief critical details can be missed. It is not a metrology or statutory-acceptance guarantee. [Gemini video understanding](https://ai.google.dev/gemini-api/docs/video-understanding) |
| Application/API | Cloud Run container for processing worker and reviewer API; Firestore or a relational store for work orders and review state | Cloud Run runs containerized services without managing infrastructure. Keep large video in object storage and metadata/state in a database. [Cloud Run docs](https://cloud.google.com/run/docs) |
| Review and evaluation | Browser dashboard with replay, structured extraction, source frame/time, reviewer correction and an evaluation set | Store model output beside the original frame and record reviewer corrections; score extraction/recapture precision against labeled sample captures before claiming accuracy. |

**Two-day project scope:** deliver one complete loop for the trench packet: Android guided capture → upload → timestamped AI suggestions and deterministic completeness checks → reviewer accept/recapture → shareable evidence packet. A polished corridor-risk map can be an alternate demo if utility footage is already available. Avoid spending the two days on a generic question-answering interface.

## Source notes

- Accelerator cohort membership is taken from each linked company’s official YC profile. The profiles also include the company’s self-described product and, where shown, its launch description.
- Company-stated performance/ROI and traction are not treated as independently verified; this report uses them only to understand the workflow and stated buyer outcome.
- India buyer hypotheses and ranking are analysis, not claims made by the reference companies. The first paid test should be interviews and a small, paid, human-reviewed pilot with a contractor/owner pair.
