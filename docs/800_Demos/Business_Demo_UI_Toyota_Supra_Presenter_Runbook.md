# Business Demo UI Toyota Supra Presenter Runbook

## Status

```text
demo: Business Demo UI Toyota Supra
status: complete
track: Business Demo Visibility Track
milestone: docs/500_Milestones/Business_Demo_UI_Toyota_Supra_v1.md
scenario_key: supra_2jz_gte_twin_turbo
primary_audience: business reviewers
latest_user_reported_business_demo_ui_toyota_supra_presenter_runbook_test_result: 5 passed
latest_user_reported_business_demo_ui_toyota_supra_presenter_runbook_test_result_on: 2026-07-10
```

## Purpose

This runbook helps present the Toyota Supra business demo to a non-technical audience.

The goal is to show the product story without requiring viewers to read terminal output, JSON files, source code, or internal milestone documents.

## Demo command

```powershell
git pull --rebase origin phase-1-cli-tooling
.\scripts\watch-business-demo-ui.ps1 -Scenario supra_2jz_gte_twin_turbo -OpenBrowser
```

## Thirty-second setup

```text
I want to show the product idea without going into implementation details.
This is not the final generated-graphics demo yet.
This is the current evidence-harness demo presented in a business-friendly browser UI.
The question is: can we make AI-generated technical graphics auditable before anyone trusts them?
```

## One-sentence product framing

```text
ConstraintOS turns a creative or technical request into a constraint-governed review process, so the output can be checked against explicit requirements before it is approved.
```

## What to show on screen

```text
1. Open the browser UI.
2. Let the auto-play run once without interruption.
3. Replay the demo and pause on each stage for explanation.
4. Point out the Toyota Supra A80 / 2JZ-GTE use case.
5. Point out the decision: needs_review.
6. Point out approval_allowed: false.
7. End on the next product step: Constraint-Driven Graphic Output Permutation POC v1.
```

## Talk track by stage

### 1. Business request

```text
This starts the way a real business request would start: someone asks for a technical graphic.
In this case, the requested subject is a Toyota Supra Mk IV / A80 twin-turbo technical graphic.
```

### 2. Loaded constraints

```text
The important part is not just the prompt.
The system has to know what must be true: Supra A80, 2JZ-GTE inline-six, sequential twin-turbo, not a generic engine.
The requirements are treated as the source of truth.
```

### 3. Candidate evidence

```text
This current demo is still fixture-only.
That means it is showing the evidence and review path, not producing final production artwork yet.
The product value is that any future generated output has to pass through this kind of evidence trail.
```

### 4. Deterministic review

```text
This is the auditability layer.
The business question is not whether AI can make something impressive.
The business question is whether the organization can tell what was checked, why it passed or failed, and whether approval is safe.
```

### 5. Decision

```text
The decision is needs_review, and approval is blocked.
That is intentional.
The system should not approve a technical graphic just because it looks plausible.
```

### 6. Next product step

```text
The next step is the product-shaped demo: generate or define constraint-derived output permutations, then validate each one.
This browser demo is the business-facing bridge from the evidence harness to that next product milestone.
```

## Expected business takeaway

```text
- ConstraintOS is not just another image generator.
- ConstraintOS is an audit and validation layer for AI-assisted publishing.
- The system makes requirements, evidence, and decisions visible.
- Automatic approval is blocked until the evidence supports it.
- The next milestone should show output permutations derived from constraints.
```

## Likely questions and answers

### Does it generate the final graphic yet?

```text
Not in this current demo.
This demo shows the review and evidence layer.
The next milestone is intended to add constraint-derived output permutations.
```

### Why is needs_review a good result?

```text
Because the system is refusing to over-trust an output.
For technical publishing, a safe review state is better than a false approval.
```

### Why use the Toyota Supra example?

```text
It is easy to understand and has specific factual constraints.
A generic engine is not good enough; the output needs to match the Supra A80 / 2JZ-GTE twin-turbo requirements.
```

### What is the commercial value?

```text
The value is reducing trust risk in AI-assisted technical publishing.
The system gives teams a repeatable way to check whether generated or proposed outputs satisfy explicit requirements before publication.
```

## Guardrails to say out loud if needed

```text
- This browser UI is static and fixture-only.
- It does not generate final graphics yet.
- It does not decode or inspect real image files.
- It does not fetch the network.
- It does not use CV/OCR.
- It does not approve candidates automatically.
```

## Closing line

```text
The demo shows the trust layer. The next milestone should show the controlled output layer.
```

## Verification command

```powershell
pytest tests/test_business_demo_ui_toyota_supra_presenter_runbook.py
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_business_demo_ui_toyota_supra_presenter_runbook.py
result: 5 passed
reported_on: 2026-07-10
assistant_ran_tests: false
```
