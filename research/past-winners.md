# Past Google AI hackathon winners: patterns and ideas

**Scope note:** The target buildathon’s exact identity and judging rubric are not assumed here. These examples are reference points from different Google/Google Cloud and India events, not evidence of the target event’s history or criteria. Verify the current event brief before committing to a direction.

## Useful precedents

| Event / source | Winner or example | What it did | Transferable signal |
|---|---|---|---|
| Google Cloud Gen AI Exchange Hackathon 2025 (India; Hack2skill’s event recap) | Team Prompt-o-nauts, YouthMind | Daily conversational check-ins, wellness risk index, tailored activity suggestions. [Recap](https://blog.hack2skill.com/gen-ai-exchange-hackathon-finale) | AI is attached to a repeatable, understandable user journey and a concrete need. The event recap lists 10 track winners, spanning youth wellness, artisan commerce, legal understanding, misinformation, careers, QA, cement operations, investment analysis, travel and governance. |
| Same event; DEI’s institutional report | Prompt-o-nauts, national winner in the youth wellness track | Added journaling and emotional insights, early distress detection, and a route to certified counsellors. [DEI report (PDF)](https://www.dei.ac.in/files/events/2025/Report%20-%20Student%20Achievement%20in%20the%20Google%20Cloud%20Gen%20AI%20Exchange%20Hackathon%202025.pdf) | Human support and responsible escalation make a sensitive AI use case more credible than a chatbot alone. Their finale presentation explicitly covered problem, working user flow, impact, scalability, and evidence for need. |
| Google Cloud Looker Hackathon (Vertex AI Edition), 2024 | Best Hack: tl;dd; Nearly Best: Dashboard Review Tool and Gemini Insight viz. [Google Cloud winners post](https://cloud.google.com/blog/products/business-intelligence/looker-2024-hackathon-winners/) | Summarized recurring dashboards and changes; reviewed dashboards for missing metrics and quality; generated human-readable summaries/forecasts from governed Looker data. | Narrow workflow integration can be compelling: use AI to remove a real recurring chore and show exactly where it fits. The winners were extensions of existing products/data, not standalone model demos. |
| Build for Bharat / ONDC (India; supporting references) | MAIT team reports first prize in the catalog digitisation theme; SSN’s newsletter describes another Build for Bharat team and “Faszen Tech” in the foundation-solution category. [MAIT report](https://www.cse.mait.ac.in/index.php/build-for-bharat-hackathon-organized-at-google-office-bangalore-kyoto), [SSN newsletter PDF](https://www.ssn.edu.in/wp-content/uploads/2025/02/Newsletter-smriti-Aug_2024.pdf) | Tackled catalog digitisation for the ONDC commerce ecosystem. | India-specific commerce infrastructure and practical digitisation are promising problem shapes. Institutional reports are secondary sources and don’t provide enough detail to reconstruct exact judging or compare projects. |
| Google Cloud × Formula E generative-AI hackathon, 2024 | No winner details used here; useful event design precedent. [Google post](https://blog.google/company-news/inside-google/around-the-globe/google-europe/united-kingdom/world-record-breaking-google-cloud-x-formula-e-hackathon/) | Teams had real video and telemetry and explored incident identification for race control; 60% of participants reportedly lacked direct AI skills. | Domain data, a specific operational decision, and an accessible starter path let teams demonstrate practical value without needing to train a model from scratch. |

## Patterns that appear reusable

1. **Start with one named user and one costly/frustrating task.** The examples address a defined job (review a dashboard, list a product, understand a legal document, route a citizen issue), rather than “AI for everyone.”
2. **Make the AI’s role inspectable.** Show inputs, sources/grounding, output, and a user action. For consequential areas, include confidence, evidence, or human review/escalation.
3. **Ship an end-to-end slice.** A polished flow that works from input through useful output and next action is easier to judge than a broad feature list. Keep a fallback path if the model fails.
4. **Use relevant data and measure a result.** Have a small representative dataset or realistic test cases. Report a baseline and a measured improvement (time saved, extraction accuracy, fewer steps, successful task completion); label synthetic data clearly.
5. **Use a platform feature where it solves an actual constraint.** The Looker examples integrate Gemini into established data workflows; Formula E supplied operational data. Google technology should be visible in a functional, explainable part of the solution rather than included as decoration.
6. **Present the user journey and evidence, not just architecture.** The DEI team’s report says their finale addressed the social problem, demonstrated system flow, and explained relevance and scalability. Build the demo around a before/after task and a real test case.
7. **Scope to the brief.** Gen AI Exchange had separate tracks and many winners. A solution that directly answers one assigned problem can fit better than a generic “AI agent” pitch. These events have different rubrics, so this is a hypothesis, not a claim about the target judging.

## Concrete directions to adapt (only if they match the actual prompt)

- **Local-language document-to-action assistant:** User uploads a government/utility/benefits notice; the system extracts deadlines and required documents, explains each step in a chosen Indian language with citations to the notice, and produces a checklist. Keep source highlights and a “verify with official source” route.
- **Small seller catalog helper:** From a product photo plus voice note, produce a multilingual listing, structured attributes and accessible alt text; seller confirms every field before publishing. Evaluate field accuracy and time-to-publish against manual entry.
- **Field-worker voice-to-case workflow:** Turn a noisy multilingual voice report into a structured case, identify missing details, and route to the right office; show the transcript, confidence, and human correction before submission. Measure completeness and handling time.
- **Grounded scheme/benefit navigator:** Ask a question over a curated set of official scheme documents, return an eligibility checklist with exact source passages and effective dates, and provide the official application link. Avoid making a final eligibility decision on behalf of the user.
- **Operations anomaly explainer:** For a provided energy, water, or logistics dataset, flag a specific anomaly, compare it with historical context, explain the likely drivers, and recommend a human-approved next check. Include a baseline and false-alarm count.

Pick the direction that best matches the actual assigned problem, available data, and a demo that can be made reliable in the time available.

## Research cautions

- “Winner” can mean overall winner, track winner, finalist, or a local GDG award. Don’t compare placements across events without checking categories.
- Hack2skill is the organizer/platform recap for Gen AI Exchange; the DEI report independently describes its own team and outcome. Treat event-wide numbers and project claims as organizer/team-reported, not independently audited.
- The MAIT and SSN pages are institutional accounts, useful corroboration but not primary judging records.
- A Google-branded event does not establish that the current buildathon uses the same platform, tracks, or scoring. Confirm the official brief first.
