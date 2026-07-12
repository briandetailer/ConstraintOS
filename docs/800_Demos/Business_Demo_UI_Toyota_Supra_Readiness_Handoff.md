# Business Demo UI Toyota Supra Readiness Handoff

## Status

```text
demo: Business Demo UI Toyota Supra
status: complete
track: Business Demo Visibility Track
scenario_key: supra_2jz_gte_twin_turbo
primary_audience: business reviewers
business_demo_ui_milestone: docs/500_Milestones/Business_Demo_UI_Toyota_Supra_v1.md
presenter_runbook: docs/800_Demos/Business_Demo_UI_Toyota_Supra_Presenter_Runbook.md
viewer_feedback_card: docs/800_Demos/Business_Demo_UI_Toyota_Supra_Viewer_Feedback_Card.md
feedback_synthesis_log: docs/800_Demos/Business_Demo_UI_Toyota_Supra_Feedback_Synthesis_Log.md
latest_user_reported_business_demo_ui_toyota_supra_readiness_handoff_test_result: 4 passed
latest_user_reported_business_demo_ui_toyota_supra_readiness_handoff_test_result_on: 2026-07-10
```

## Purpose

Use this handoff when preparing to show the Toyota Supra browser demo to a business reviewer.

This is the shortest path from a clean repo checkout to a non-technical demo conversation.

## One-command demo path

```powershell
git pull --rebase origin phase-1-cli-tooling
.\scripts\watch-business-demo-ui.ps1 -Scenario supra_2jz_gte_twin_turbo -OpenBrowser
```

## What the viewer should see

```text
- A browser-based ConstraintOS business demo.
- A Toyota Supra A80 / 2JZ-GTE twin-turbo use case.
- A staged story: business request -> loaded constraints -> candidate evidence -> deterministic review -> decision -> next product step.
- A visible needs_review decision.
- approval_allowed: false.
- A clear statement that final generated graphics are not included yet.
```

## What to say first

```text
This is not the final generated-graphics demo yet.
This shows the trust layer: how ConstraintOS makes requirements, evidence, and decisions visible before anyone approves an AI-assisted technical graphic.
```

## Minimum presenter path

```text
1. Open the browser demo.
2. Let auto-play run once.
3. Replay it and pause on each stage.
4. Explain that the Toyota example matters because a generic engine is not good enough.
5. Explain that needs_review is intentional because technical publishing should not over-trust plausible-looking outputs.
6. Ask the viewer whether they want to see output permutations next.
7. Capture feedback on the viewer feedback card.
```

## After the demo

```text
1. Fill out or transcribe the viewer feedback card.
2. Classify the signal as strong_business_signal, mixed_business_signal, or weak_business_signal.
3. Update the feedback synthesis log.
4. If a reviewer understands the trust-layer story and asks for generated or candidate outputs, prioritize Constraint-Driven Graphic Output Permutation POC v1.
```

## Verification status

```text
business_demo_ui_test: 8 passed
presenter_runbook_test: 5 passed
viewer_feedback_card_test: 5 passed
feedback_synthesis_log_test: 4 passed
readiness_handoff_test: 4 passed
assistant_ran_tests: false
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_business_demo_ui_toyota_supra_readiness_handoff.py
result: 4 passed
reported_on: 2026-07-10
assistant_ran_tests: false
```

## Local verification

```powershell
pytest tests/test_business_demo_ui_toyota_supra.py
pytest tests/test_business_demo_ui_toyota_supra_presenter_runbook.py
pytest tests/test_business_demo_ui_toyota_supra_viewer_feedback_card.py
pytest tests/test_business_demo_ui_toyota_supra_feedback_synthesis_log.py
pytest tests/test_business_demo_ui_toyota_supra_readiness_handoff.py
```

## Guardrails

```text
- Browser UI only.
- Static fixture-only walkthrough.
- No generated final graphics.
- No constraint-derived graphic output permutations yet.
- No real local image input.
- No image decoding.
- No pixel inspection.
- No CV/OCR provider integration.
- No network fetch.
- No automatic approval.
```
