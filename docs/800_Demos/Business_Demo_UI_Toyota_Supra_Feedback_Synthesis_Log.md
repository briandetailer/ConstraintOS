# Business Demo UI Toyota Supra Feedback Synthesis Log

## Status

```text
demo: Business Demo UI Toyota Supra
status: complete
track: Business Demo Visibility Track
milestone: docs/500_Milestones/Business_Demo_UI_Toyota_Supra_v1.md
presenter_runbook: docs/800_Demos/Business_Demo_UI_Toyota_Supra_Presenter_Runbook.md
viewer_feedback_card: docs/800_Demos/Business_Demo_UI_Toyota_Supra_Viewer_Feedback_Card.md
scenario_key: supra_2jz_gte_twin_turbo
primary_audience: business reviewers
latest_user_reported_business_demo_ui_toyota_supra_feedback_synthesis_log_test_result: 4 passed
latest_user_reported_business_demo_ui_toyota_supra_feedback_synthesis_log_test_result_on: 2026-07-10
```

## Purpose

Use this log after collecting one or more viewer feedback cards from the Toyota Supra browser demo.

The goal is to turn business-reviewer reactions into a clear decision about what the next demo must prove.

## What this log synthesizes

```text
- whether viewers understood the ConstraintOS product idea
- whether the trust / auditability value was clear
- whether the Toyota Supra A80 / 2JZ-GTE example helped explain constraints
- whether the needs_review decision made sense
- whether viewers asked to see output permutations next
- whether reviewers connected the demo to real publishing, compliance, brand, engineering, or documentation workflows
```

## Reviewer signal table

| Reviewer | Product idea understood? | Business value clear? | needs_review made sense? | Asked for output permutations? | Real workflow identified? | Signal |
| --- | --- | --- | --- | --- | --- | --- |
| _pending reviewer_ | _pending_ | _pending_ | _pending_ | _pending_ | _pending_ | _pending_ |

## Signal definitions

```text
strong_business_signal:
- reviewer understands trust / auditability value
- reviewer can explain why automatic approval should be blocked
- reviewer asks to see output permutations next
- reviewer connects the product to a real review, publishing, compliance, brand, engineering, or documentation workflow

mixed_business_signal:
- reviewer understands the basic idea but needs a more concrete output example
- reviewer sees value but cannot yet identify a buying or workflow context
- reviewer likes the UI but wants stronger proof that constraints affect outputs

weak_business_signal:
- reviewer thinks this is only a prettier JSON viewer
- reviewer does not understand why needs_review is useful
- reviewer expects final image generation immediately and misses the validation-layer value
- reviewer cannot identify a real business workflow where the trust layer matters
```

## Synthesis notes template

```text
review_session:
reviewer_count:
strong_signal_count:
mixed_signal_count:
weak_signal_count:
clearest_part:
most_confusing_part:
business_workflows_named:
requests_for_next_demo:
recommended_next_action:
```

## Decision rule

```text
If at least one business reviewer understands the trust-layer story and asks to see generated or candidate outputs, prioritize:
Constraint-Driven Graphic Output Permutation POC v1

If reviewers do not understand needs_review, improve the presenter runbook and browser copy before building output permutations.

If reviewers understand the value but want a concrete output example, prioritize a fixture-safe output-permutation demo rather than real image generation.
```

## Current recommended next action

```text
pending_viewer_feedback
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_business_demo_ui_toyota_supra_feedback_synthesis_log.py
result: 4 passed
reported_on: 2026-07-10
assistant_ran_tests: false
```

## Guardrails

```text
- This synthesis log is documentation-only.
- This log does not authorize generated final graphics.
- This log does not authorize real local image input.
- This log does not authorize image decoding, pixel inspection, CV/OCR, or automatic approval.
- This log can recommend the next gated milestone, but it does not implement new runtime capability.
```

## Local verification

```powershell
pytest tests/test_business_demo_ui_toyota_supra_feedback_synthesis_log.py
```
