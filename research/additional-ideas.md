# Additional startup ideas

13 November 2026. These are separate from the agent-services marketplace and traveler-carry marketplace; both remain shortlisted. Ideas are hypotheses rather than validated gaps. Competitor pages indicate product positioning, not verified performance or market traction. The third founder's experience is not yet included.

## 1. Repair Passport: diagnosis-to-parts workflow for independent technicians

A technician photographs a device label and faulty part, describes symptoms in their preferred language, and receives an editable job card plus a list of candidate parts and sources. Compatibility must be verified by the technician, not guessed by AI. Customer: independent repair shop or service chain; proposed revenue: shop subscription or supplier referral with disclosure. Demo: three synthetic repair cases, two catalogues and evidence-linked part matching. Gemini parses labels/voice; deterministic model numbers constrain matches. Existing [SparesX](https://www.sparesx.com/) and [SETBIN](https://setbin.in/) already serve repair technicians; the differentiator must be demonstrably better compatibility or a narrow repair workflow, not merely another marketplace. Main unknown: access to reliable parts data and willingness to pay.

## 2. SiteProof: construction delivery and issue reconciliation

A small contractor photographs a delivery slip and material at a site; the system extracts item, quantity and supplier, compares to a purchase order, and drafts a discrepancy for human approval. Buyer: subcontractor or construction supplier; subscription per site is a hypothesis. Gemini handles document and photo understanding; rules compare quantities and units, with explicit unknowns. Demo on a mock PO, delivery slip and photos. [Arisinfra's SEBI filing](https://www.sebi.gov.in/sebi_data/attachdocs/aug-2024/1723620609645_396.pdf) describes established tech-enabled procurement and delivery workflows, so check its and other offerings before claiming novelty. Main risk: a photo cannot prove weight or quality; no automatic acceptance/rejection.

## 3. WaterLedger: verify water deliveries for buildings

For an apartment manager, combine a delivery slip, timestamp, tank-level sensor and manual confirmation into a delivery record; flag unexplained discrepancies for review. AI extracts records and explains anomalies; deterministic sensor calculations and an uncertainty band underpin estimates. Buyer: apartment association or campus facilities operator. A demo can replay synthetic sensor readings and invoices; water-level change alone is not a reliable measurement if usage or pumps are active. Existing [WaterApp](https://psa.gov.in/CMS/web/sites/default/files/2025-12/Water%20Technology%20Compendium.pdf) offers water monitoring and automation; its installation/savings figures are provider-reported. Validate whether delivery verification is truly an unmet paid need and whether calibrated measurements are possible.

## 4. Factory quality evidence

At a single small supplier, inspect one type of part with a camera; show potential defect to a human, attach the lot number, and track corrective action. Buyer: quality manager. Gemini turns human notes into an evidence-linked ticket; a tested vision model assists, not replaces, inspection. A prototype can use a small labelled set with held-out examples. [WEF/PSA SME playbook](https://www.psa.gov.in/CMS/web/sites/default/files/publication/WEF_Transforming_Small_Businesses_2025.pdf) identifies quality management as an AI application. Existing visual inspection vendors mean the wedge is a specific workflow and customer access. Need real defect data, accuracy evaluation and a factory partner. Details: [deep B2B research](deep-b2b.md).

## 5. Drain inspection to work order

A field worker photographs a visible blocked drain. The app records location, suggests a review priority and creates a maintenance task with before/after photos. Buyer: campus or industrial park facilities manager. Gemini organizes field notes; image detection needs testing. Demo with staged images, a work list and before/after evidence. [MoHUA's storm-water manual](https://mohua.gov.in/upload/uploadfiles/files/Draft%20Volume-2%20Part%20B-Operation%20%26amp%3B%20Maintenance%20and%20Part%20C-Management.pdf) discusses routine inspections; [Fluid Robotics](https://frontiertech.niti.gov.in/story/monitoring-billion-litres-daily-the-tech-platform-powering-smarter-urban-water-systems/) already provides water-infrastructure monitoring. Main unknown: whether facilities managers want and pay for a dedicated workflow. No flood-prevention claim from a demo. Details: [deep industry research](deep-industry.md).

## 6. Voice-to-service handoff for field technicians

An equipment service worker records a voice note and photo after a visit. The system drafts a structured service record, flags missing serial number or readings, and shows citations to the input for review. Buyer: pump, HVAC, solar or industrial maintenance firms. Proposed fee per technician per month. Gemini transcription and multimodal extraction do real work; synthetic examples suffice for demo. Existing field-service management platforms offer job cards and automation; investigate their voice and local-language capabilities with target customers. Validate noise, code-switching, inaccurate extraction and willingness to change existing WhatsApp workflows. Do not recommend unsafe electrical repairs.

## Comparison and next step

Factory quality and technician workflows best match the CVs' industrial, edge and full-stack experience, conditional on user access. SiteProof and WaterLedger give visually understandable demos but need operational verification. Repair Passport is a consumer-adjacent marketplace with direct existing competitors. Drain inspection has a compelling physical workflow but institutional sales friction. None is proven new or validated.

Interview 3 users per top two ideas, asking about the last occurrence, existing workaround, time/cost, purchase authority, and permission to review a representative example. Test whether Gemini materially improves that workflow and identify a small two-day demo. Avoid claiming customers, pilots or performance before observed.
