# Business Demo UI Toyota Supra Viewer Feedback Card

## Status

```text
demo: Business Demo UI Toyota Supra
status: complete
track: Business Demo Visibility Track
milestone: docs/500_Milestones/Business_Demo_UI_Toyota_Supra_v1.md
presenter_runbook: docs/800_Demos/Business_Demo_UI_Toyota_Supra_Presenter_Runbook.md
scenario_key: supra_2jz_gte_twin_turbo
primary_audience: business reviewers
latest_user_reported_business_demo_ui_toyota_supra_viewer_feedback_card_test_result: 5 passed
latest_user_reported_business_demo_ui_toyota_supra_viewer_feedback_card_test_result_on: 2026-07-10
```

## Purpose

Use this card immediately after showing the Toyota Supra browser demo to a business reviewer.

The goal is to collect business-facing signal without asking the reviewer to inspect terminal output, JSON files, source code, or internal milestone documents.

## Reviewer context

```text
You just watched a browser demo of ConstraintOS using a Toyota Supra A80 / 2JZ-GTE twin-turbo technical graphic use case.

The demo was intentionally fixture-only. It did not generate the final graphic yet.

The demo showed how ConstraintOS makes the request, constraints, evidence, and decision visible before approval.
```

## Quick rating

```text
1. I understood the product idea.
   [ ] Strongly agree
   [ ] Agree
   [ ] Unsure
   [ ] Disagree

2. The demo made the business value clear.
   [ ] Strongly agree
   [ ] Agree
   [ ] Unsure
   [ ] Disagree

3. The Toyota Supra / 2JZ-GTE example helped me understand why constraints matter.
   [ ] Strongly agree
   [ ] Agree
   [ ] Unsure
   [ ] Disagree

4. The needs_review decision made sense.
   [ ] Strongly agree
   [ ] Agree
   [ ] Unsure
   [ ] Disagree

5. I would want to see the next demo showing constraint-derived output permutations.
   [ ] Strongly agree
   [ ] Agree
   [ ] Unsure
   [ ] Disagree
```

## Open feedback

```text
What was the clearest part of the demo?


What was confusing or too technical?


What business problem did this seem closest to solving?


What would you need to see before believing this could be useful in a real workflow?


Would a generated-output demo make this more compelling? Why or why not?
```

## Signal classification

```text
strong_business_signal:
- reviewer understands trust / auditability value
- reviewer can explain why automatic approval should be blocked
- reviewer asks to see output permutations next
- reviewer connects the product to a real review, publishing, compliance, brand, engineering, or documentation workflow

weak_business_signal:
- reviewer thinks this is only a prettier JSON viewer
- reviewer does not understand why needs_review is useful
- reviewer expects final image generation immediately and misses the validation-layer value
- reviewer cannot identify a real business workflow where the trust layer matters

next_demo_signal:
- reviewer asks to see multiple candidate outputs
- reviewer asks how constraints change the output
- reviewer asks how failed outputs are rejected
- reviewer asks whether this can be used outside automotive examples
```

## What not to promise

```text
- Do not promise generated final graphics in the current demo.
- Do not promise real local image input in the current demo.
- Do not promise image decoding, pixel inspection, CV/OCR, or automatic approval in the current demo.
- Do not describe the fixture-only browser UI as production software.
```

## Recommended follow-up

```text
If the reviewer understands the trust-layer story and asks for generated or candidate outputs, route that feedback to:
Constraint-Driven Graphic Output Permutation POC v1
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_business_demo_ui_toyota_supra_viewer_feedback_card.py
result: 5 passed
reported_on: 2026-07-10
assistant_ran_tests: false
```

## Local verification

```powershell
pytest tests/test_business_demo_ui_toyota_supra_viewer_feedback_card.py
```
