# Three additional product directions

13 November 2026. Working concepts, not validated markets, inventions, or verified Shark Tank participants. They preserve the buildathon constraint of meaningful Google AI plus Google Cloud deployment. Existing B2A/traveler candidates and the previous program research remain available. User has confirmed access to robotics/AI researchers; broader customer access is unknown.

## 1. BenchPilot: debug the circuit on the desk

A learner has the correct circuit diagram but their assembled circuit does not work. The product combines a fixed camera view, an explicit schematic and actual multimeter readings, builds a partial observed connection graph and helps distinguish wiring hypotheses with a small number of approved measurements. It should mark hidden connections unknown rather than infer them confidently.

Buyer hypothesis: electronics teaching labs, makerspaces and educational kit vendors. Value hypothesis: reduce instructor troubleshooting time while teaching a repeatable diagnostic method. Begin with one supported breadboard/kit, not arbitrary electronics or appliance repair.

Google role: Gemini interprets visible component labels and maps a learner's description to a structured fault hypothesis; a constrained graph/measurement engine checks the hypothesis; Gemini explains the next approved test with evidence. FastAPI runs on Cloud Run and observations are stored per session. The diagram, expected measurements and actual instrument observations remain separately visible.

Two-day proof: one low-voltage circuit, several deliberately inserted faults, an overhead phone camera and manual meter readings or an already available instrument connection. Demonstrate a wrong-row connection that is visually ambiguous but resolved by a continuity reading. Report fault identification, false diagnoses and measurements required on held-out faults against a checklist and generic multimodal assistant. Only isolated, current-limited training fixtures; do not expand the demo to mains, high-energy batteries or uncontrolled remote power changes.

Competition: [Flux](https://docs.flux.ai/flux/Introduction/learn-electronics) supports AI-assisted electronics learning/design; [Circuit Mind](https://www.circuitmind.io/platform) supports schematic automation; [Imula](https://imula.io/) advertises natural-language instrument workflows and is accepting a waitlist. Imula's marketing does not establish production availability, but does establish a direct competing concept. Generic AI instrument control is therefore not differentiation. The initial hypothesis is one instructor-approved, novice-oriented physical wiring and measurement workflow with demonstrable educational value. inspectAR is another important comparison; an older FAQ link redirected to Cadence's general resource page during the primary agent's check, so exact current functionality needs confirmation.

Kill if measurements cannot be obtained reliably, the board mapping is brittle, novices can solve it as quickly using the fixed checklist, or the lab will not pay. This is the strongest of the three for the team's technical skills and a measurable buildathon demonstration.

## 2. DiagramBridge: explore a STEM diagram as a structure

A teacher uploads a simple circuit, flowchart or node-link diagram. The system extracts objects, labels and relationships into an editable graph. The teacher approves it; a blind learner can navigate nodes and connections using keyboard/audio, ask spatial questions grounded in the graph and access a simplified print-ready vector version.

Start with one diagram family, such as simple circuits. A prose image description alone does not give persistent node-by-node navigation, and a connection error can reverse the meaning of a diagram. Preserve uncertainty and teacher edits as part of the product.

Buyer hypothesis: college disability-support centres, accessible-content publishers and transcription services. The first value test is preparation time and learner comprehension, not a generic image-description demo.

Google role: Gemini proposes labels and relations from the supplied image; deterministic checks validate the graph schema and connectivity; Cloud Run serves the editor and accessible player. Spoken questions can use Gemini Live if it improves navigation. A printed SVG is not automatically a usable tactile graphic; tactile adaptation requires specialist review.

Two-day proof: three permitted diagrams, explicit teacher correction of an incorrectly extracted edge, keyboard navigation and answers generated from the corrected graph. A proof of extraction/editing is feasible; actual accessibility benefit requires testing with blind users. Do not describe it as an independently validated learning tool.

Competition: [TADA](https://arxiv.org/abs/2311.04502) already demonstrates touch/audio exploration of node-link diagrams. [Chart4Blind](https://arxiv.org/abs/2403.06693) converts charts to accessible outputs. [Mathpix](https://docs.mathpix.com/guides/accessible-pdf) supports accessible document conversion, with stated limitations on figure descriptions. Therefore navigation, accessibility exports and conversion are not inventions here. The proposed entry point is teacher-reviewed conversion of a narrowly selected curriculum diagram type; unproven unmet need and sales path.

Status: ambitious exploration, not a leading event recommendation without a co-design partner. Drop if existing tools already meet the teacher's need or graph correction takes as long as manual authoring.

## 3. PatternPatch: turn specific fabric remnants into cutting kits

A tailor or upcycler places a flat remnant on a calibrated mat, marks grain/defects, selects an approved accessory pattern and receives a cutting arrangement with seam allowance and remaining inventory. The output is a physically usable cut plan for the cloth already on hand.

Buyer hypothesis: small upcycling studios, costume departments, fashion schools or reuse stores. Revenue could be software subscription or kit preparation, but neither is validated. No universal fabric/material recognition or bespoke garment-fitting promise.

Google role: Gemini helps identify visible markings, interpret user intent and choose among reviewed templates; computer vision produces a user-correctable outline; deterministic geometry performs packing and collision checks; Cloud Run serves the workflow. If an ordinary outline-and-nest tool gives the same result, the AI role may be too weak for this event.

Two-day proof: three real remnants, a printed calibration target, simple pouch/panel patterns and a measurable manual-layout baseline. Print or draw the plan at scale and verify pieces fit. Never substitute visually pleasing generative artwork for a dimensionally valid pattern.

Competition is substantial: [SeamScape](https://seamscape.com/software/cutting) explicitly offers camera capture followed by nesting on irregular material. [Aeronaut SiliconEye](https://www.aeronaut.co/technology/machine-vision/siliconeye) traces scraps and nests patterns. [ScrapFit](https://scrapfit.webbe-b.com/) offers remnant/defect/grain-aware cut planning. This is not a novel algorithm or feature bundle. The possible opportunity is an inexpensive end-to-end service for small operators without cutting machinery, but the evidence does not establish incumbents exclude them.

Status: lowest priority of these three; retain only if actual tailors show a gap in current products, material recovered exceeds labor/capture cost and AI improves the workflow. A local-language interface alone is insufficient.

## Additional candidates screened out in this pass

- Generic badminton video coach: [LynseeAI](https://lynseeai.com/en/) and [ShuttleSense](https://www.shuttlesense.com/) already sell closely related analysis/review. A distinct customer or technical advantage was not established.
- Generic recipe/allergen assistant: [Apicbase](https://get.apicbase.com/recipe-management-software/) already integrates recipe extraction, suppliers, costs and allergen data. No new recommendation.
- Generic print-artwork checker: [GlobalVision](https://www.globalvision.co/industries/print-and-packaging) already covers artwork comparison and print workflow integration.
- Generic Indian music practice AI: [NaadSadhana](https://www.naadsadhana.com/) and [Narottam](https://vipular.github.io/narottam.github.io/) demonstrate existing accompaniment and teaching approaches.

## Decision

BenchPilot is the best next technical experiment from this batch; DiagramBridge needs direct accessible-design collaboration; PatternPatch needs strong local customer evidence to survive the competitive overlap. These are not three equally strong recommendations. Detailed preliminary research is in [fresh-idea-competition.md](fresh-idea-competition.md). No implementation, interviews or external outreach occurred.
