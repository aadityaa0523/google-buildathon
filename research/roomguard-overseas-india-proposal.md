# RoomGuard: an overseas-proven model to test in India

14 November 2026. Working name only; no trademark or domain check. This is a concrete new candidate for the user's request for an interesting real-world problem and Google Buildathon solution, not a claim of validated commercial success or India-first invention.

## Recommendation and problem statement

Build an affordable, remotely monitored bedbug detection service for hotel rooms. Begin with a hotel group and its existing pest-management contractor. A small trap containing enclosed optics should identify possible insect captures, alert the correct staff, and track inspection and subsequent monitoring.

**Problem statement:** Hotels need to discover bedbugs between manual inspections, before a guest encounters them. Physical monitors already exist, but staff must reliably check them; a missed or delayed inspection can delay response. The proposed product reduces that monitoring gap. Whether the reduction is worth the price in Indian hotels remains to be established.

This is more concrete than an insect-identification app: it requires continuous physical observation, validated capture and classification, device maintenance, and timely response. A general AI chat cannot observe a hidden insect by itself.

## Evidence and competition

| Finding | Evidence and interpretation |
|---|---|
| Overseas operating model | UK company Spotta reports 225 installed Bed Pods at London's Bankside Hotel, with a named maintenance-manager testimonial. This is vendor-published deployment evidence, not audited profitability. [Spotta customer account](https://www.spotta.co/post/marriott-bankside-hotel-impressed-with-spotta-featured-in-daily-mail) |
| Alternative foreign implementation | Finland's Valpas uses connected bed legs and a hotel service proposition. A customer, Sokos Hotel Puijonsarvi, describes its use. The model is already commercial abroad. [Hotel customer page](https://www.sokoshotels.fi/en/hotels/kuopio/original-sokos-hotel-puijonsarvi/valpas-technology) |
| Relevant India problem | Rentokil PCI describes hotel bedbug introduction and reputational consequences, and offers inspection/treatment. This supports an existing service category, not measured Indian incidence or our monitoring budget. [India hotel guidance](https://www.rentokil-pestcontrolindia.com/services/commercial-pest-control/hospitality/hotel-pest-prevention) |
| Direct Indian alternative | GPA announced India distribution of UK DOT's BugScents Sentry Pro in August 2026. The product uses a physical lure/trap; DOT's public instructions describe checking it after placement. Thus India already has early-detection monitors. [Distributor launch](https://giridharpaiassociates.com/2026/08/05/expanding-indias-non-toxic-ipm-toolkit-giridhar-pai-associates-partners-with-digital-odour-technologies-dot-uk-to-launch-bugscents-sentry-pro/), [manufacturer instructions](https://www.digitalodourtechnologies.com/sentry-pro) |
| Powerful existing distribution | Rentokil PCI provides bedbug treatment and monitoring/follow-up. It could partner, compete, import or bundle. Do not assume a large incumbent will distribute a new entrant's product. [India bedbug service](https://www.rentokil-pestcontrolindia.com/plp/pest-control-bed-bugs-treatment) |

No verified India deployment/distributor for Spotta or Valpas was located in this bounded search. Their availability to Indian buyers remains unknown. A foreign company can sell directly even without an indexed Indian office. **Do not pitch this as India's first bedbug detector or the world's first smart pest monitor.**

Full supporting checks: [India competition](bedbug-india-competition.md), [commercial/technical assessment](bedbug-commercial-check.md).

## Product and differentiation to test

1. **Retrofit monitored trap:** enclosed macro optics observe only the trap interior. No camera view of guests. Use a compatible, validated trap/lure through a supplier partnership or independently engineered hardware; modifying a trap must not compromise its biological effectiveness.
2. **Room-specific evidence:** model marks possible targets and uncertain images; a qualified reviewer confirms an incident. Staff see the room, original image and action status.
3. **Device-health signal:** lost connectivity, exhausted battery, obscured optics or maintenance overdue are distinct from no detection. Never represent an offline device as a clean room.
4. **Response and continued observation:** housekeeping and the pest contractor acknowledge inspection, record findings and continue monitoring after treatment. Lack of capture does not prove eradication.

The proposed India positioning is retrofit affordability and lower inspection effort for multi-property operators. These are **engineering and commercial targets**, not established advantages over Spotta, Valpas or local monitored-trap offerings. Automatic alerts are already part of overseas products; the opportunity is an execution/localization business, not global technical novelty.

## Google Buildathon demonstration

The [official event page](https://startupbuildathon.com/) calls for a new AI product using Google AI and deployed on Google Cloud; it evaluates product potential, market viability, architecture and depth of Google use along with founder profile. The proposed architecture fits those published technical requirements if implemented. Linked portal conditions remain incompletely verified in the earlier [rules check](buildathon-rules-recheck.md). Accept the user-reported deadline extension for planning.

- **Vertex AI:** train/evaluate an image classifier on licensed, expert-labelled trap images; retain an uncertain/unknown class and human confirmation. Google documents custom image-classification workflows. [Official Google example](https://colab.research.google.com/github/GoogleCloudPlatform/vertex-ai-samples/blob/main/notebooks/official/migration/sdk-automl-image-classification-batch-online.ipynb)
- **Gemini:** convert housekeeping voice notes into structured inspection records, connect them to the detected event, and draft next steps from a pest professional's approved SOP. No autonomous pesticide prescriptions.
- **Cloud Run, Cloud Storage and Firestore:** proposed backend, image storage, property/device/event state and review dashboard. These are design choices; no deployment has occurred.

The demo should show a physical enclosed camera, a known specimen or labelled replay, and the chain from capture evidence to review and staff acknowledgement. Include a non-target insect/lint example and an offline-device example. If images or events are replayed, label them. It demonstrates the sensing/review workflow, not room-scale early detection or infestation prevention.

The actual technical challenge is capturing insects reliably and making accurate decisions under real room conditions. The camera model does not solve capture probability. India deployments need local species/life-stage validation, suitable placement across bed designs, low-power connectivity, cleaning procedures and controlled evaluation. Do not introduce live pests into occupied rooms to demonstrate the product.

## Business model and scale assumptions

Initial customer: hotel group operations/housekeeping head, with a pest-management provider involved in installation and response. Sell device installation or rental plus a per-room monitoring subscription. Treatment can remain with the existing contractor. This avoids assuming treatment revenue or operational capability we do not have.

Illustrative price to test: ₹150 per room per month, with installation/hardware charged separately or explicitly amortized. This is not a market quote or validated willingness to pay.

| Paying monitored rooms | Annual subscription revenue at illustrative price |
|---|---:|
| 5,000 | ₹90 lakh |
| 50,000 | ₹9 crore |
| 100,000 | ₹18 crore |

Revenue is not profit. Hardware depreciation/replacement, consumables, batteries, gateway/connectivity, image inference, review labour, site visits and channel commissions all matter. For example, a hypothetical ₹1,500 device amortized over 24 months costs ₹62.50 per month before those other expenses. Actual hardware cost and service life have not been quoted. Frequent technician visits could make a ₹150 plan unviable.

Customer ROI must compare subscription/install cost against reduced manual inspection effort and conservatively attributable losses avoided. Use lost room **contribution margin**, not all room revenue, and avoid counting refunds and foregone revenue twice. Reputation effects are hard to attribute and should not rescue otherwise weak economics.

Hotels are the first segment. Hostels, co-living and sleeper transport may extend the opportunity but have different price sensitivity, fixtures, connectivity and service needs; they are not validated demand. We have not established a billion-dollar market or that 100,000 rooms are realistically obtainable. A broader pest platform would require additional hardware and biological validation by species.

## Tests that make this a startup rather than a demo

1. Obtain current inspection labour, complaint, treatment and room-closure records from consenting hotels. Confirm the budget owner and price sensitivity.
2. Compare against a commercially available monitor plus its scheduled inspection protocol, not an artificially weak no-monitor baseline. Obtain actual Spotta/Valpas/import and local product quotes before claiming lower cost.
3. Run expert-supervised capture/classification tests with local species and look-alike insects. Split evaluation by physical trap/site/time rather than adjacent frames of the same insect.
4. Track false alerts per 1,000 room-nights, confirmed detection delay, missed captures, uptime, maintenance time and response time. A small pilot with no confirmed infestations cannot prove sensitivity.
5. Seek one paid multi-room pilot, then a repeat deployment. Stop if installation or servicing makes unit economics unattractive or existing providers already supply the same outcome at a better cost.

The defensible asset could become field-tested hardware, local trap-image data, reliability and the hotel/contractor channel. None exists yet. The recommended next commitment is a focused prototype and buyer test, not manufacturing inventory.

## Other overseas models screened this pass

- Ting-style electrical fire warning: meaningful overseas insurer deployment, but SafeGuard AI, Honeywell India and Schneider India already advertise relevant electrical-risk/arc-fault products. Rejected as an India-first proposition. [SafeGuard](https://safeguardai.in/), [Honeywell India](https://www.honeywellbuildings.in/fire/fire-detection-and-alarm-system/electrical-fire-monitoring), [Schneider India catalog](https://www.se.com/in/en/download/document/CA909014/).
- Retail cooler failure response: real operational problem but sensor/alert competitors exist and the proposed response workflow is insufficiently distinctive. See [exploratory scan](overseas-realworld-a.md).
- Grease-trap servicing and water-leak survey triage: legitimate jobs, but the proposed incremental workflow features did not meet this user's novelty bar. See [exploratory scan](overseas-realworld-b.md). These agent suggestions are not finalists.
