# Shark Tank and accelerator analysis for the Google buildathon

13 November 2026. Decision synthesis for Aadityaa and Kanak. Third CV pending. This is the final ranking for this research pass; it overrides the preliminary rankings in the three source reports. Previously shortlisted B2A and traveler marketplaces remain recorded, but this report searches for additional directions.

## Conclusion

Eighteen source startups were screened: six Shark Tank India, six Shark Tank US and six YC companies. **The user confirmed access to robotics or AI researchers during this research. That moves FieldBench, a task-specific physical-AI evaluation/data service, to first priority for this team.** Guided evidence capture for underground utility work is second, conditional on finding a contractor and accepting engineer. Phone-video dairy follow-up is a distant third and requires a vet and appropriate footage. None is established as unique, underserved in India or validated by customers. Access to researchers does not establish purchasing budget.

The outcome is deliberately not a forced list of five recommendations. Several initially attractive ideas failed the competition check. Appearing on television or joining an accelerator is not proof that a deal closed, that a company became profitable or that a derivative idea will win this competition.

[Rules and Google capability review](buildathon-rules-recheck.md) documents the official site, deadline, incomplete linked terms and implementation constraints.

## BeforeCover: capture underground work while evidence is visible

**Reference:** [sizeless, YC Summer 2023](https://www.ycombinator.com/companies/sizeless). Its stated product converts footage of open trenches into spatial documentation and work records. Treat its precision/traction claims as company claims; our proposal does not reproduce its mature reconstruction stack in two days.

**Customer situation:** A water/fiber contractor finishes a connection. Once the trench is covered, the owner-side engineer cannot inspect a missed detail without another visit or excavation. Proposed product: guide the crew through required capture, identify visible components, flag missing evidence, preserve measured observations and let the owner approve or request recapture before cover. Link the accepted record to the specific work order and billing item. The primary commercial hypothesis is fewer rejected work records and repeated visits, not automatic regulatory compliance or faster payment guaranteed by AI.

**What Google does:** Android capture; Gemini interprets permissioned video/voice and proposes component labels/timestamped evidence; Cloud Run hosts processing/review; Storage preserves originals; Firestore records work-item and approval state. Optional ARCore Depth on a supported phone supports an explicitly approximate spatial visualization. Human-entered/calibrated measurements remain authoritative.

**48-hour core proof:** Build a tabletop pipe fixture with a known work plan and scale markers. Capture three runs: complete, missing a required connection view, and blurred/occluded. Show the system requesting recapture while the fixture is accessible, then reviewer acceptance with evidence tied to bill items. Include a spatial/component view only if it can be measured against known geometry. It must not be a generic video summary followed by a PDF.

**Evaluation:** For held-out captures, measure required-view detection, false acceptance, component-label accuracy and time to a reviewable packet. If testing geometry, report error against known dimensions separately. Compare with a generic Gemini prompt plus manual capture checklist. Claim only observed results.

**Competition and India evidence:** [vGIS vSite](https://www.vgis.io/vsite/) already combines utility capture, field records, AI, QA and quantity workflows; Android availability alone is not differentiation. A [TCIL-hosted BSNL tender](https://www.tcil.net.in/tender/pdf/25f2436_1.pdf), in the indexed Measurement Book Management section, calls for GIS/mobile AI-video measurements and independent-engineer validation. The indexed passage supports relevance in Indian procurement; it does not prove award, implementation, current availability or unmet demand. The full PDF timed out during review. Our initial customer should be a reachable private-campus or smaller subcontractor/owner pair, not a national government tender.

**Possible advantage to test:** A minimal, low-cost capture/acceptance workflow that fits one contractor's actual work-order format and existing engineer review. This remains a hypothesis until we check current tools and pricing with that pair.

**Decision:** Advance to interviews. Need a contractor AND the person accepting the records. Drop if customers already have a working equivalent, only certified survey outputs are accepted, or a checklist gives the same benefit. A surveying or civil engineering adviser is needed for production scope; the CVs establish software/CV skills, not surveying expertise.

## FieldBench: first priority given confirmed researcher access

**Reference:** [Human Archive, YC Winter 2026](https://www.ycombinator.com/companies/human-archive), a physical-world data company with explicitly stated India operations. This is emphatically not an overseas model absent from India. Its existence demonstrates the business mechanism, not our right to copy data or proof of demand for our niche.

**Customer situation:** A robotics or vision-agent developer needs a repeatable test set for a particular task, such as identifying whether components were sorted into the correct bins under occlusion, poor light and viewpoint changes. Generic web video does not necessarily provide the required task specification, labels or failure coverage.

**Proposed product:** A task owner specifies a capture contract, edge cases and acceptance criteria. Consenting contributors record the requested task. The system checks coverage/quality, routes ambiguous clips to human review, and delivers a versioned dataset, labels and evaluation report. Start as a narrow managed evaluation service; do not build a broad gig marketplace before obtaining a buyer. Revenue hypothesis: per accepted dataset/evaluation package.

**What Google does:** Android capture; Gemini proposes task/event labels and missing-case suggestions; deterministic checks handle format/duration; Cloud Storage holds approved clips; Firestore tracks consent, task coverage and review; Cloud Run runs QA and benchmark jobs. Human adjudication establishes ground truth. Do not use one model's unverified generated labels to claim that model performs well.

**48-hour core proof:** Record 12–20 original clips of one benign task with controlled variation. Hold out clips before tuning. Show a requested dataset contract, an unusable/occluded clip rejected for recapture, human correction of a false AI label, and a packaged benchmark that reveals a real failure of a baseline vision agent. Simulate contributor payments clearly if shown; no recruitment or commercial collection is performed in this research.

**Defensibility hypothesis:** Repeated access to a specific task environment, reliable rights/consent, consistent annotation and measured coverage. A website accepting uploads has little advantage. Human Archive and data-service vendors are direct/adjacent competitors; a vertical benchmark must be explicitly requested by a buyer.

**Additional competition and free substitutes:** [Scale's Physical AI offering](https://scale.com/physical-ai) already combines collection and annotations, and [Toloka](https://toloka.ai/physical-ai-become-a-data-partner) recruits physical-work data partners. [DROID's research release](https://arxiv.org/abs/2403.12945) provides open robot demonstrations; [LeRobot](https://huggingface.co/docs/lerobot/index) supplies collection tools, shared datasets and policy workflows. Selling generic clips or a dataset uploader fails our filter. The proposed advantage must be a buyer-specified missing evaluation slice, an accepted collection protocol and fast, independently checked delivery. Competition in full physical evaluation also exists; this is not a new research category.

**Scope distinction:** RGB phone video can support visual task/event evaluation. It is not equivalent to robot action/state trajectories, force/tactile measurements or proof of closed-loop robotic success. If a lab requires these, use its existing rig and supported logs or change the target task; do not invent telemetry. A phone-only demo should be pitched as a visual-agent evaluation product.

**Decision:** First customer-discovery priority now that the user confirms researcher access. Advance only if a lab defines a missing dataset and a budget owner sees value. Strong fit to Kanak's evaluations and both founders' CV/Android experience. This also provides a concrete possible service category for the existing B2A marketplace idea.

**Five interview prompts for the user's contacts:**

1. What is the last real-world case where your model failed despite a good benchmark score? Ask for a non-confidential example.
2. Which required task, environment or failure case is absent from your current data and DROID/LeRobot or other public sources?
3. Do you need RGB clips, synchronized depth/action logs, or actual robot trials? What exact acceptance criteria would make collected data usable?
4. What did you last spend in time or money collecting/labeling such data, and who controls a budget for outsourcing it?
5. Would you review a small held-out sample and use a test report? What would make you reject it or pay for a larger run?

Pass only if a reachable researcher supplies a concrete missing case, approves a protocol the team can execute and connects us to a credible paying unit. If everyone only wants free public data or cannot use phone footage, do not build the broad marketplace. No interview has yet been conducted and none of these contacts has been messaged.

## HerdFollow: standardized video follow-up for dairy veterinarians

**Reference:** [Brainwired WeSTOCK](https://www.brainwired.in/) identifies its Shark Tank India appearance and livestock monitoring product. The adaptation is a visiting field worker's phone-based repeat-visit record, not a claimed replacement for its wearable technology.

**Proposed product:** Capture an animal's identifier and a standardized walk clip, maintain comparable visits, record a veterinarian's observations and flag missing/unusable follow-up evidence. Any learned mobility observations are candidate measurements requiring veterinarian validation. No automated diagnosis, pregnancy detection or treatment advice.

**Google implementation:** Android capture and explicit animal tag/QR; Gemini for capture guidance, observable-event summaries and evidence links; Cloud Run/Storage/Firestore for case history and clinician review. If building quantitative gait analysis, use a genuinely suitable animal model and measured labels. MediaPipe's human pose model is not an animal-health solution.

**48-hour proof:** A small licensed or consented set of repeated animal clips; show capture-quality checks, correct animal-to-visit association and a vet-review comparison. Without field access and validated labels, the demo proves workflow only. Do not call synthetic scores validated health predictions.

**Competition check:** [Stellapps mooON](https://www.stellapps.com/mooon/) already combines wearable monitoring and herd management in India. [CattleEye](https://cattleeye.com/en-gb) and [GEA](https://www.gea.com/en/stories/gea-minimizes-dairy-cow-lameness-with-ai-solution/) describe camera-based mobility/body-condition monitoring. Therefore, cameras without animal wearables are not a new category. The only proposed opening is standardized intermittent field-worker capture for a specific small-herd vet network; adoption, breed/camera robustness and price are unproven.

**Decision:** Conditional, below the first two. No vet/data access means do not choose it for this event. This is not a stronger general recommendation than the original B2A candidate merely because it appeared on Shark Tank.

## Screen of all 18 references

These rows describe adaptations we considered, not necessarily products offered by the reference company. Source and participation links are in the linked reports.

| Source startup / program | Mechanism or adaptation considered | Final call |
|---|---|---|
| sizeless / YC S23 | Evidence collected before underground work is covered; shared acceptance/billing record | Advance, subject to contractor and engineer access |
| Human Archive / YC W26 | Commission physical-world task data with QA and benchmark outputs | Advance only with a defined lab buyer |
| WeSTOCK / Shark Tank India | Repeated animal observation and veterinary follow-up | Conditional; camera competitors and field validation are substantial |
| Kanopy / YC F26 | Corridor imagery into maintenance priorities and completion verification | Alternate if utility data exists; calibrated geometry and procurement are hard |
| XMachines / Shark Tank India | Agricultural contractor work verification from logs and video | Hold; actual machine integration is the core, mock telemetry does not prove it |
| PadCare / Shark Tank India | Sanitary-waste collection evidence and service management | Deprioritize; collection/recycling is the source company's hard part, software-only derivative needs demand evidence |
| BabyQuip / Shark Tank US | Equipment rental with local fulfillment; proposed condition history | Deprioritize; Indian rental supply exists and AI photos do not establish product safety/cleanliness |
| CoatChex / Shark Tank US | Item custody; proposed multimodal lost-property recovery | Reject generic version after direct NotLost/Boomerang competition check |
| Kibo / Shark Tank India | Accessible documents and audio | Reject generic scanner/translator; direct product overlap |
| Aignosis / Shark Tank India | AI developmental screening | Reject as two-day lead; direct overlap and clinical/data requirements |
| Atypical Advantage / Shark Tank India | Inclusive hiring | Reject generic matching; weak distinctiveness and sensitive automated ranking |
| DARTdrones / Shark Tank US | Mission-specific drone training | Reject generic version; operating credentials/data/competition dominate |
| Rescue Ready / Shark Tank US | Fire-escape product plus readiness | Reject derivative safety-plan generator; physical/code-critical function not reproduced |
| CoinOut / Shark Tank US | Receipt rewards and a downstream data payer | Reject OCR-plus-points; economics and distribution are the business |
| Remento / Shark Tank US | Prompted voice memories into printed keepsakes | Reject generic memoir generator under the user's current filter |
| Tenyks / YC S21 | Existing cameras into restaurant operations intelligence | Deprioritize until a specific unmet metric/buyer is found |
| Cerrion / YC S22 | Factory events linked to avoided downtime | Deprioritize without factory partner and an accessible process |
| Dream / YC S26 | Asset condition across handovers | Deprioritize generic vehicle inspection; Indian competitors already active |

## Corrections after the parallel research

The preliminary US report gave lost-property search a higher rank. Further primary sources show [NotLost](https://notlost.com/) already offers photo recognition, enquiry matching and return logistics; [Boomerang](https://thanksboomerang.com/how-it-works/) also provides matching and recovery. The generic adaptation fails our difference test.

The preliminary India report ranked PadCare operations first. I disagree with that ranking for this user: a waste-visit checklist with image labels does not yet demonstrate a compelling gap or AI advantage. Do not open waste containers to stage a demo, infer hidden contents from a closed bin or claim proof of recycling from a pickup photograph. Use clean staged props if the workflow is ever evaluated.

The accelerator report initially had only adjacent competitors for underground capture. vGIS and the TCIL indexed tender above are more directly relevant. Their presence strengthens evidence that the workflow matters while weakening any novelty claim. Existing Android apps mean Android alone is not a distinguishing feature.

## How to turn a candidate into an application

1. State one customer and the last real occurrence of the problem; obtain this from an interview, not our inference.
2. Name the closest existing product and the specific reason a reachable customer cannot/will not use it.
3. Show a working Google-powered action that changes the outcome, with a deployed backend and observable failure handling.
4. State the paid unit and likely acquisition route. Do not turn interview interest into claimed revenue or traction.
5. Demonstrate on held-out inputs, compare against a capable generic AI baseline, and show limitations plainly.

Preferred next interview: the robotics/AI researchers the user can reach, to specify FieldBench's first evaluation task and identify a buyer. BeforeCover becomes the alternative if contractor/engineer access develops. No messages were sent to anyone.

## Research files

- [Buildathon site and Google capabilities](buildathon-rules-recheck.md)
- [Shark Tank India: six references](shark-tank-india-opportunities.md)
- [Shark Tank US: six references](shark-tank-global-opportunities.md)
- [YC: six references](accelerator-startup-opportunities.md)
- [Previous top five](top-five-shortlist.md)

This pass covers Shark Tank India, Shark Tank US and Y Combinator. It does not claim an exhaustive review of Dragons' Den, Techstars, every TV pitch or every accelerator company. Third-party directories were used only for discovery; key program/product findings were checked against broadcaster, company, accelerator or incubator sources. Reported company performance is not independently audited.
