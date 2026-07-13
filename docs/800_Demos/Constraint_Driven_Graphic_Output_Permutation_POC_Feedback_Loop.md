# Constraint-Driven Graphic Output Permutation POC Feedback Loop

## Status

```text
demo: Constraint-Driven Graphic Output Permutation POC
status: feedback-loop-defined
phase_status: complete
track: Business Demo Visibility Track
milestone: docs/500_Milestones/Constraint_Driven_Graphic_Output_Permutation_POC_v1.md
reviewer_handoff: docs/800_Demos/Constraint_Driven_Graphic_Output_Permutation_POC_Reviewer_Handoff.md
watch_script: scripts/watch-constraintos-output-poc.ps1
phase: Phase 5 - feedback loop
scenario_key: supra_2jz_gte_twin_turbo
primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic
implementation_authority: documentation-only-feedback-loop
latest_user_reported_constraint_driven_graphic_output_permutation_reviewer_handoff_rerun_test_result: 5 passed
latest_user_reported_constraint_driven_graphic_output_permutation_reviewer_handoff_rerun_test_result_on: 2026-07-13
latest_user_reported_constraint_driven_graphic_output_permutation_feedback_loop_test_result: 6 passed
latest_user_reported_constraint_driven_graphic_output_permutation_feedback_loop_test_result_on: 2026-07-13
assistant_ran_tests: false
```

## Purpose

Collect reviewer feedback after the output-permutation browser demo and convert it into a scoped next-step decision.

This feedback loop evaluates whether reviewers understand the product story:

```text
loaded constraints -> controlled output permutations -> deterministic validation -> needs_review
```

## What reviewers should inspect first

```text
runs/output-poc/supra_2jz_gte_twin_turbo/<timestamp>/index.html
```

For the latest user-reported run:

```text
D:\Code\ConstraintOS\runs\output-poc\supra_2jz_gte_twin_turbo\20260712-151228\index.html
```

The generated `index.html` is the business-facing artifact. The JSON files are supporting evidence for technical reviewers.

## Reviewer feedback card

Ask each reviewer these questions after the browser demo:

```text
1. Did the four-step flow make sense?
   - Constraints loaded
   - Output permutations
   - Deterministic validation
   - needs_review

2. Was it clear that ConstraintOS is defining controlled output specifications from requirements?

3. Was it clear why every variant remains needs_review?

4. Was it clear why approval_allowed remains false?

5. Which output permutation was easiest to understand?
   - turbo_system_focus
   - inline_six_engine_identity_focus
   - technical_label_density_focus
   - reviewer_safe_minimal_focus

6. Which output permutation felt most product-relevant?

7. What did the reviewer expect to see next?
   - richer fixture-safe placeholder outputs
   - clearer evidence summaries
   - more visual browser polish
   - real generated artwork
   - real image validation
   - other

8. Did the guardrails feel like a strength, a limitation, or both?
```

## Feedback classification

Classify each response as one of these signals:

```text
strong_product_signal:
- Reviewer understands constraints -> permutations -> validation -> needs_review.
- Reviewer can explain why approval remains blocked.
- Reviewer asks to see richer fixture-safe output examples or more polished placeholder visualization.

mixed_product_signal:
- Reviewer understands the idea but still expects real generated graphics immediately.
- Reviewer sees value but cannot explain needs_review without prompting.
- Reviewer wants a simpler story or clearer visual sequence.

weak_product_signal:
- Reviewer does not understand why permutations exist.
- Reviewer interprets the page as a failed image-generation demo.
- Reviewer cannot distinguish fixture-safe specifications from generated artwork.
```

## Decision rules

```text
If strong_product_signal dominates:
- Move to a fixture-safe visual placeholder refinement milestone.
- Preserve deterministic output specifications.
- Improve the browser page before adding any real image authority.

If mixed_product_signal dominates:
- Improve the browser story and reviewer handoff first.
- Add clearer labels explaining that this is controlled output specification, not production artwork.
- Do not expand runtime scope yet.

If weak_product_signal dominates:
- Pause feature expansion.
- Rework the business demo narrative around trust, constraints, and approval blocking.
- Keep all output generation and real-image behavior out of scope.
```

## Accepted next-step candidates

These are allowed next actions if feedback supports them:

```text
- Fixture-safe visual placeholder refinement.
- Browser walkthrough polish.
- Reviewer copy simplification.
- Better evidence summary cards.
- Stronger traceability between constraints, permutations, and validation evidence.
```

## Explicitly blocked next-step candidates

These are not authorized by this feedback loop:

```text
- Real generated final graphics.
- Production artwork generation.
- Real local image input.
- local_file_path loading.
- file_uri loading.
- Artifact download.
- Network fetch.
- Image decoding.
- Pixel inspection.
- CV/OCR provider integration.
- Automatic approval.
```

## Feedback synthesis format

Use this format after collecting feedback:

```text
reviewer_count:
strong_product_signal_count:
mixed_product_signal_count:
weak_product_signal_count:
clearest_permutation:
most_product_relevant_permutation:
most_common_confusion:
most_requested_next_step:
recommended_decision:
recommended_next_milestone:
approval_allowed: false
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_constraint_driven_graphic_output_permutation_feedback_loop.py
result: 6 passed
reported_on: 2026-07-13
assistant_ran_tests: false
```

## Phase 5 done criteria

```text
[x] Feedback loop document exists.
[x] Reviewer feedback questions are defined.
[x] Feedback classification labels are defined.
[x] Decision rules are defined.
[x] Accepted next-step candidates are scoped.
[x] Blocked next-step candidates are listed.
[x] Feedback synthesis format is defined.
[x] Guardrails are preserved.
[x] Verification test result recorded.
```

## Verification command

```powershell
pytest tests/test_constraint_driven_graphic_output_permutation_feedback_loop.py
```