# Shark Tank US concepts → India buildathon opportunities

**Review status:** Preliminary source research. [The final synthesis](startup-programs-google-buildathon.md) supersedes these rankings. Direct competition from [NotLost](https://notlost.com/) and [Boomerang](https://thanksboomerang.com/how-it-works/) downgrades generic lost-property matching; Gear Passport remains a weak, unvalidated operations adaptation, not a lead recommendation.

Research date: 13 November 2026. Scope: six actual Shark Tank US participants, verified against ABC's official “Appeared on Shark Tank” list or its episode recaps. Participation does not imply a deal, endorsement, or success; no outcomes are called “wins.” The list itself cautions that ABC does not endorse listed products.

## Shortlist

| Rank | Overseas mechanism | India adaptation worth testing | Preliminary call |
|---|---|---|---|
| 1 | BabyQuip: local operator network rents, delivers, sets up and insures baby gear | A safety/condition passport for existing small rental providers, not another rental marketplace | Best business mechanism; validate whether providers will pay for trust/claims workflow |
| 2 | CoatChex: fast, ticketless item handoff with retrieval/recovery | AI-assisted lost-property search and custody evidence for high-volume event venues | Interesting, but cloakroom tech already exists; narrow to searchable item evidence and prove venue pain |
| 3 | DARTdrones: mission-specific drone training and organizational adoption | No recommendation: drone training/inspection stack is already active in India | Good pattern, weak whitespace |
| 4 | Rescue Ready: fire escape ladder plus family-focused safety education | No recommendation for a 48-hour AI build: physical/code-critical safety is the product | Clear need category, unsafe to fake expertise with AI |
| 5 | CoinOut: receipt capture subsidized by retailer/transaction data and rewards | No recommendation: likely loyalty/receipt-capture clone | Crowded consumer incentives; hard to establish payer/data economics |
| 6 | Remento: voice-first prompts transformed into a keepsake book | Reject for this brief | Too close to generic voice capture/transcription/story generation |

## 1. BabyQuip → rental-item safety and condition passport

**Show and product.** ABC's Season 11, Episode 14 recap names BabyQuip and describes its vetted, insured local providers delivering and setting up cribs, car seats, strollers and toys. BabyQuip's current first-party About page describes a provider marketplace, 500,000+ reservations, and insurance covering the rental experience. Those are company-reported numbers, not independently audited. Sources: [ABC episode recap](https://abc.com/news/ba065dce-182c-45a7-80bc-a57ef45075da/category/2887649), [BabyQuip About](https://www.babyquip.com/about).

**India alternatives / gap hypothesis.** Baby gear rental already exists: Goa provider My Tiny Traveller advertises delivery, setup and sanitization; Babyseal offers local rentals in Kerala; RentNEarn lists baby strollers. So a BabyQuip clone is not a gap. A narrower hypothesis is that small rental operators lack an easy, auditable chain of custody for item model/serial, cleaning, inspection, damage, repair, and retirement. Verify this with providers before treating it as a problem. Sources: [My Tiny Traveller](https://www.mytinytraveller.com/), [Babyseal](https://babyseal.in/), [RentNEarn](https://www.rentnearn.com/).

**Concept.** *Gear Passport*: Android workflow for an operator to scan/photograph a gear label at onboarding, attach a human-approved model and checklist, then capture condition and cleaning evidence at each handoff. Gemini can read visible label text and structure user-supplied observations; deterministic rules and a human remain authoritative for safety, recalls, cleaning completion, and retirement. Do not let a model declare a car seat or crib safe from a photo.

**Payer / 48-hour proof.** Payer: independent rental providers or a hotel/concierge with its own inventory. Demonstrate 3 demo items through intake → clean/inspect → dispatch → return → damage flag; show model label OCR, photo-paired before/after evidence and an exportable item history. This proves an operational transaction, not a dashboard. Ask 3 local providers whether this replaces a real spreadsheet/WhatsApp step and what they would pay for.

**Google fit.** Gemini multimodal image understanding for label extraction and structured condition notes; Android capture; Firebase/Firestore for item-event records and offline access; Cloud Run for the API. Keep staff confirmation on every extracted field. [Gemini image understanding docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/image-understanding), [Firestore offline access](https://firebase.google.com/docs/firestore/manage-data/enable-offline), [Cloud Run quickstart](https://docs.cloud.google.com/run/docs/quickstarts/deploy-container).

**Risk.** The strongest value would be safety and trust, but AI image interpretation can be wrong and equipment checks are safety-critical. The pitch must be verifiable records and reminders, never automated safety certification. Local rental supply is already present; this is an unvalidated B2B workflow hypothesis.

## 2. CoatChex → visual lost-property recovery for event venues

**Show and product.** ABC's Season 4, Episode 2 recap explicitly features CoatChex. It describes a technology-enabled coat-check business focused on security, efficiency and convenience. Current business model/status is not assumed from the old recap. Source: [ABC episode recap](https://abc.com/news/6fa9b206-7c9e-4abf-ae01-46a931d4a9e1/category/939724).

**India alternatives / gap hypothesis.** India has luggage storage networks (Lugsto), cloakroom/locker providers, and event ticketing/check-in apps such as Unifesto. Digital coat-check products also exist internationally. Therefore “QR cloakroom” alone is neither new nor whitespace. The preliminary hypothesis was ambiguous lost-property claims at venues; direct matching competitors identified in the final synthesis substantially weaken it. Sources: [Lugsto](https://www.lugsto.com/), [Unifesto](https://www.unifesto.app/), [CoatCheck product](https://www.coatcheck.app/product/coatcheck).

**Concept.** *Found at the Venue*: every deposited or found item gets a tag, timestamp, photo and short voice description; staff can search “black laptop sleeve with red logo” and see likely photo matches. This is multimodal retrieval over that venue's own inventory, paired with a QR claim code and staff-confirmed release—not face recognition or generalized event software.

**Payer / 48-hour proof.** Payer: venue operator or event production company paying per event/venue. Demo 30 synthetic items, ingest item photo + spoken Hindi/English description, retrieve a claimed match, show evidence and close custody. Instrument retrieval time and false matches. Only proceed if an event operator confirms this is a recurring high-cost failure; otherwise the wedge is too small.

**Google fit.** Gemini multimodal extraction/translation plus embeddings or structured descriptions for venue-scoped search; Android camera/voice input; Firestore for tickets and sync; Cloud Run API. Require staff approval before item release. Risk: incumbents already automate tags and QR retrieval, and exact visual similarity can fail for generic objects.

## 3. DARTdrones → drone training and mission operations

**Show and product.** ABC's official appeared-on list includes Dart Drones; the company's first-party site says “As Seen on ABC's Shark Tank.” DARTdrones sells basic and mission-specific training for mapping, inspections, disaster response, thermal imaging and search/rescue. Sources: [ABC appeared-on list](https://abc.com/news/920582c3-2083-45bc-81c9-95e33c5a76e9/category/706923), [DARTdrones](https://www.dartdrones.com/), [training system](https://www.dartdrones.com/drone-training-system/).

**India alternatives / gap hypothesis.** India already has DGCA-certified training and an industrial drone-inspection ecosystem; AIRPIX advertises inspection, analysis and an established drone fleet. This makes a generic drone-training or visual-inspection product a poor bet. Possible niche only after customer proof: mission-specific field checklists and evidence review for a single underserved operator segment. Sources: [AIRPIX](https://airpix.in/drone-inspection.html), [DGCA drone portal](https://digitalsky.dgca.gov.in/).

**Payer / demo / Google fit.** Potential payer is an enterprise operator, training provider or drone service firm. A two-day proof could let a trainee upload an inspection sequence and get a human-reviewed completeness checklist with cited frames, but that risks becoming a report generator. Google fit is Gemini video/image input, Android capture, Cloud Run. **Reject as current recommendation:** mature Indian competition, regulatory and data dependencies, and weak novelty without access to a real operator.

## 4. Rescue Ready → home fire escape ladder and safety education

**Show and product.** ABC's Season 11, Episode 23 recap identifies Rescue Ready as creators of fire escape ladders and safety education. Source: [ABC episode recap](https://abc.com/news/0209277c-5d48-4bfa-991b-7e46588ef74b/category/2887649).

**India adaptation considered.** A building-specific evacuation readiness exercise for hostels/PGs could map who needs help, identify blocked exits, and log drills. Payer might be a school/hotel/hostel operator. But route advice and fire-safety compliance are life-critical, and a two-day demo cannot validate code applicability, floor-plan accuracy, or safe egress. **Reject for hackathon build** unless a certified fire-safety partner supplies and approves the rules. Do not market a Gemini-generated evacuation plan as safe.

## 5. CoinOut → consumer receipt capture and rewards

**Show and product.** ABC's official appeared-on list includes CoinOut. Its own terms describe rewards earned by scanning receipts and other activity; the product uses receipt data/rewards as its acquisition loop. Sources: [ABC appeared-on list](https://abc.com/news/920582c3-2083-45bc-81c9-95e33c5a76e9/category/706923), [CoinOut terms](https://coinout.com/pages/terms).

**India adaptation considered.** OCR that reads small-shop receipts and gives consumers rewards could support merchant insights, but retailer-funded reward economics, fraud, receipt formats and privacy are the core business—not the OCR demo. India already has broad cashback and merchant loyalty products. **Reject:** a receipt scanner with points is an easy clone and the payer is unclear. A more defensible B2B tax/compliance workflow would be a different business and is outside this inspiration.

## 6. Remento → voice-first family memoirs

**Show and product.** ABC's appeared-on list includes Remento. Its current first-party site sends prompts by text/email, converts recordings into edited stories and prints a book with QR-linked audio. Sources: [ABC appeared-on list](https://abc.com/news/920582c3-2083-45bc-81c9-95e33c5a76e9/category/706923), [Remento product](https://www.remento.co/).

**India adaptation considered.** Multilingual oral history with voice-preserving keepsakes is viable as a consumer product, but a recording/transcription/summarization pitch is exactly the crowded/generic direction this brief rules out. **Reject** unless a specific paying institutional workflow (e.g. a museum's consented oral-history archive and curation pipeline) is validated; do not just translate Remento.

## Recommendation

Prototype **Gear Passport** first if the team can speak with even two rental operators. Its differentiated mechanism is operating local inventory with delivery/cleaning and trust, while the proposed AI is bounded to extracting and retrieving evidence. The Goa and Kerala examples prove supply exists, so adoption is a hypothesis rather than an “India has no solution” claim.

Keep **Found at the Venue** as the alternative if the team has event-venue access. It has a stronger quick demo but a smaller and more crowded wedge. In either case, make the AI do a visible, consequential task in the transaction, deploy the API to Cloud Run, and leave high-stakes decisions with a human. The evidence collected here is desk research only; talk to prospective payers before choosing.

## Primary / high-value sources

- [ABC Shark Tank appearances index](https://abc.com/news/920582c3-2083-45bc-81c9-95e33c5a76e9/category/706923)
- [ABC BabyQuip appearance recap](https://abc.com/news/ba065dce-182c-45a7-80bc-a57ef45075da/category/2887649)
- [ABC CoatChex appearance recap](https://abc.com/news/6fa9b206-7c9e-4abf-ae01-46a931d4a9e1/category/939724)
- [BabyQuip's current business model](https://www.babyquip.com/about)
- [My Tiny Traveller's current Goa offer](https://www.mytinytraveller.com/)
- [Gemini image understanding on Google Cloud](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/image-understanding)
