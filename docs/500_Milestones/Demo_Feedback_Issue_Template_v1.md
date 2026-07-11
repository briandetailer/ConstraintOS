# Demo Feedback Issue Template v1

## Status

```text
milestone: Demo Feedback Issue Template v1
status: complete
started_on: 2026-07-10
completed_on: 2026-07-10
track: Business Demo Visibility Track
previous_context: Current Evidence-Harness POC Demo Feedback Packet complete
baseline: 487 passed
latest_user_reported_demo_feedback_issue_template_test_result: 4 passed
latest_user_reported_demo_feedback_issue_template_test_result_on: 2026-07-10
```

## Purpose

Make structured current POC demo feedback easier to collect directly through GitHub Issues.

The current evidence-harness demo already has a feedback packet. This milestone adds a GitHub issue template so friends, early reviewers, and technical peers can submit critique without manually copying the Markdown feedback form.

## Scope

```text
- Add .github/ISSUE_TEMPLATE/demo-feedback.md.
- Preserve current-demo context: evidence-harness POC, not final graphics-output demo.
- Capture reviewer context.
- Capture one-sentence product understanding.
- Capture demo-flow critique.
- Capture evidence-file clarity.
- Capture needs_review result clarity.
- Capture future graphic-output permutation expectations.
- Capture accessibility and technical trust feedback.
- Capture product risk, strongest idea, and next-step recommendations.
- Include feedback labels for sorting.
- Preserve guardrail reminder.
- Add tests.
- Update command reference.
```

## Implemented files

```text
.github/ISSUE_TEMPLATE/demo-feedback.md
tests/test_demo_feedback_issue_template.py
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
docs/500_Milestones/Demo_Feedback_Issue_Template_v1.md
```

## Verification command

```powershell
pytest tests/test_demo_feedback_issue_template.py
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_demo_feedback_issue_template.py
result: 4 passed
reported_on: 2026-07-10
assistant_ran_tests: false
```

## Issue template boundary

```text
current_demo_type: evidence-harness POC demo
current_demo_result: needs_review
approval_allowed: false
future_target_bank: Constraint-Driven Graphic Output Permutation POC v1
not_currently_supported:
- generated final graphics
- constraint-derived graphic output permutations
- arbitrary local image input
- image decoding
- CV/OCR provider integration
- unrestricted image generation/editing
- automatic approval
```

## Guardrails

```text
- GitHub issue template only.
- No new processing capability added.
- No new byte-loading source added.
- No local image file opening.
- No artifact download.
- No network fetch.
- No image decoding.
- No CV/OCR provider choice.
- No image generation.
- No image editing.
- No automatic candidate approval.
- Do not claim tests passed unless actually run.
```

## Done criteria

```text
[x] Demo feedback issue template exists.
[x] Template captures reviewer context.
[x] Template captures demo-flow critique.
[x] Template captures evidence-file critique.
[x] Template captures needs_review clarity.
[x] Template captures future output expectations.
[x] Template captures accessibility and technical trust feedback.
[x] Template captures product critique.
[x] Template includes feedback labels.
[x] Template includes guardrail reminder.
[x] Tests added.
[x] Command reference updated.
[x] Verification test result recorded.
```
