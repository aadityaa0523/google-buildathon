# Buildathon website recheck

Checked 13 November 2026. Public website plus linked terms; not a complete application-dashboard audit. No application submitted or organizer contacted.

## Event page

The [official page](https://startupbuildathon.com/) asks for a new AI-powered product using Google AI and deployment on Google Cloud. It evaluates founder profile, product potential, market viability, architecture and Google usage. Applications close 13 November; city builds are 20–21 November; finale is 2 December. Applications include idea, solution, architecture and deck. Solo founders and teams can apply; the FAQ states no team-size limit. Each top-ten team receives $5,000 cash and $5,000 credits, subject to terms/taxes. The tool list is illustrative: no requirement to use every listed product or published scoring weights was found.

## Linked terms need clarification

The [linked terms](https://hack2skill.com/event/buildathon/tnc) rendered in-browser but not through web text extraction. It contains incomplete event/client placeholders. Its IP section describes a six-month right of first refusal over exclusive licensing, with a 30-day organizer response period, plus disclosure/marketing rights. Do not assume finalized applicability, unrestricted IP, or equity-free terms. Clarify the applicable agreement with the organizer before submitting valuable IP. This is a description of the displayed text, not a legal determination.

The organizer's [LinkedIn page](https://in.linkedin.com/company/hack2skill) displayed an application-deadline post specifying 11:59 PM IST on 13 November. The event site itself states the date without a cutoff time.

## Unresolved details

No verified event-specific rule was found here establishing whether prior code is permitted, the exact repository/demo-video submission format, mandatory open-source licensing, ownership terms superseding the generic template, team-member eligibility restrictions beyond the landing page, or guaranteed pre-event credits. Do not import rules from a different Google competition. The investor-interest form is not the participant application.

## Implementation interpretation

The proposed approach is to implement one consequential AI function and deploy the working API and review flow on Cloud Run. React, FastAPI, conventional computer vision and deterministic business rules can support that architecture; the public page does not establish an all-Google dependency requirement. This is a planning interpretation, not organizer approval of a specific stack. Confirm actual model access and quota before choosing a demo; listing a product name does not establish account access.

## Verified Google building blocks

| Product | Documented capability | Appropriate role and limit |
|---|---|---|
| [Gemini video understanding](https://ai.google.dev/gemini-api/docs/video-understanding) | Processes video and can reference timestamps | Suggest events/components with evidence frames. Does not certify dimensions, physical safety, medical status or truth. |
| [Gemini Live](https://ai.google.dev/gemini-api/docs/live) | Real-time audio/image interaction and tool use | Guided capture and spoken feedback when latency helps the task. Optional, not a rule requirement. |
| [Cloud Run](https://cloud.google.com/run/docs/overview/what-is-cloud-run) | Managed execution of application code/containers | Host FastAPI, jobs and reviewer service. Include a functioning deployed endpoint, not just a proposed architecture. |
| [Cloud Storage](https://cloud.google.com/storage/docs/introduction) | Object storage | Keep original permissioned media and generated artifacts with access controls. |
| [Firestore](https://firebase.google.com/docs/firestore) | Application document database and synchronization | Store work orders, labels, review states and dataset manifests. Large videos belong in object storage. |
| [Document AI](https://cloud.google.com/document-ai/docs/overview) | OCR, document classification and structured extraction | Optional input extraction for a work order or invoice. Not needed merely to increase the number of Google logos. |
| [ARCore Depth](https://developers.google.com/ar/develop/depth) | Depth information on supported devices | Optional spatial prototype with calibration and reported errors. Not automatic survey-grade measurement. |
| [MediaPipe Pose](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker) | Human body landmarks in image/video | Suitable for consented human-motion experiments; not an off-the-shelf cattle pose or health model. |

## Demonstration requirements we impose, not event rules

One complete customer action; permissioned or clearly labelled synthetic input; a held-out test set; a comparison against a capable generic AI baseline; an observable failure and recovery; a plausible payer; and no claims that simulated payments, hardware telemetry or review decisions are live integrations. These are our quality gates responding to the user's filtering request.
