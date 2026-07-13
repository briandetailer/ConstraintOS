# Constraint-Driven Graphic Output Permutation POC v1

## Status

```text
milestone: Constraint-Driven Graphic Output Permutation POC v1
status: kickoff-ready
kickoff_status: complete
phase_1_contract_status: complete
phase_2_toyota_fixture_data_status: complete
phase_3_watch_script_status: complete
phase_4_browser_demo_status: ready-to-show
phase_5_feedback_loop_status: complete
started_on: 2026-07-10
track: Business Demo Visibility Track
previous_demo_package: Business Demo UI Toyota Supra
previous_handoff: docs/800_Demos/Business_Demo_UI_Toyota_Supra_Readiness_Handoff.md
primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic
scenario_key: supra_2jz_gte_twin_turbo
implementation_authority: gated-fixture-safe-only
feedback_loop: docs/800_Demos/Constraint_Driven_Graphic_Output_Permutation_POC_Feedback_Loop.md
latest_user_reported_constraint_driven_graphic_output_permutation_poc_test_result: 9 passed
latest_user_reported_constraint_driven_graphic_output_permutation_poc_test_result_on: 2026-07-12
latest_user_reported_constraint_driven_graphic_output_permutation_watch_script_test_result: 9 passed
latest_user_reported_constraint_driven_graphic_output_permutation_watch_script_test_result_on: 2026-07-12
latest_user_reported_constraint_driven_graphic_output_permutation_reviewer_handoff_test_result: 5 passed
latest_user_reported_constraint_driven_graphic_output_permutation_reviewer_handoff_test_result_on: 2026-07-12
latest_user_reported_constraint_driven_graphic_output_permutation_reviewer_handoff_rerun_test_result: 5 passed
latest_user_reported_constraint_driven_graphic_output_permutation_reviewer_handoff_rerun_test_result_on: 2026-07-13
latest_user_reported_constraint_driven_graphic_output_permutation_feedback_loop_test_result: 6 passed
latest_user_reported_constraint_driven_graphic_output_permutation_feedback_loop_test_result_on: 2026-07-13
latest_user_reported_constraint_driven_graphic_output_permutation_browser_demo_run_created: true
latest_user_reported_constraint_driven_graphic_output_permutation_browser_demo_run_created_on: 2026-07-12
latest_user_reported_constraint_driven_graphic_output_permutation_browser_demo_run_dir: D:\Code\ConstraintOS\runs\output-poc\supra_2jz_gte_twin_turbo\20260712-151228
latest_user_reported_constraint_driven_graphic_output_permutation_browser_demo_index_html: D:\Code\ConstraintOS\runs\output-poc\supra_2jz_gte_twin_turbo\20260712-151228\index.html
latest_user_reported_constraint_driven_graphic_output_permutation_browser_demo_final_decision: needs_review
latest_user_reported_constraint_driven_graphic_output_permutation_browser_demo_approval_allowed: false
assistant_ran_tests: false
assistant_ran_demo: false
```

## Purpose

Create the next product-shaped POC after the Toyota business demo: a fixture-safe workflow that shows how loaded constraints can define multiple graphic output permutations and then validate each permutation against those constraints.

The business demo proved the trust layer. This milestone starts the controlled output layer.

```text
input constraints + scenario instructions -> graphic output permutations -> validation evidence -> reviewable result
```

## Why this comes next

The current Toyota business demo is ready to show, but it intentionally stops before final generated graphics.

Business reviewers now need a more concrete answer to this question:

```text
Can ConstraintOS define or generate multiple candidate outputs from the same requirements, then explain which ones need review, fail, or are closest to acceptable?
```

## Product promise for this milestone

```text
- Use the Toyota Supra A80 / 2JZ-GTE use case.
- Load scenario constraints.
- Produce fixture-safe graphic output permutations or output specifications.
- Show how each permutation differs.
- Validate each permutation against explicit requirements.
- Preserve traceability from requirement -> permutation -> evidence -> review decision.
- End with final_decision: needs_review.
- Preserve approval_allowed: false.
```

## Intended business-visible outputs

```text
graphic-output-manifest.json
- Lists each fixture-safe output permutation.
- Explains the business-readable intent of each permutation.
- Links each permutation to loaded constraints.

graphic-output-permutations.json
- Defines controlled output variants.
- Example variants may include cutaway emphasis, drivetrain emphasis, turbo-system emphasis, or label-density emphasis.
- Each variant remains fixture-safe and deterministic.

graphic-output-validation.json
- Records which constraints each permutation satisfies, misses, or leaves uncertain.
- Defaults uncertainty to needs_review.

graphic-output-review-packet.json
- Summarizes the result for a non-technical reviewer.
- Explains why approval remains blocked.
```

## Initial Toyota Supra output permutation examples

```text
1. turbo_system_focus
   Business intent: show why the output must represent a sequential twin-turbo 2JZ-GTE rather than a generic engine.

2. inline_six_engine_identity_focus
   Business intent: show why the output must remain a 2JZ-GTE inline-six and not drift into V6, V8, rotary, RB26, LF4, or B58 geometry.

3. technical_label_density_focus
   Business intent: show how the same constraints can produce a clearer or denser technical publishing variant.

4. reviewer_safe_minimal_focus
   Business intent: show a conservative output specification that exposes only validated requirements and leaves uncertain elements in needs_review.
```

## Demo command

```powershell
.\scripts\watch-constraintos-output-poc.ps1 -Scenario supra_2jz_gte_twin_turbo -OpenBrowser
```

## Run folder

```text
runs/output-poc/<scenario>/<timestamp>/graphic-output-manifest.json
runs/output-poc/<scenario>/<timestamp>/graphic-output-permutations.json
runs/output-poc/<scenario>/<timestamp>/graphic-output-validation.json
runs/output-poc/<scenario>/<timestamp>/graphic-output-review-packet.json
runs/output-poc/<scenario>/<timestamp>/index.html
runs/output-poc/<scenario>/<timestamp>/run-metadata.json
```

## Latest user-reported browser demo run

```text
source: user-reported local script run
command: .\scripts\watch-constraintos-output-poc.ps1 -Scenario supra_2jz_gte_twin_turbo -OpenBrowser
result: browser run created
run_dir: D:\Code\ConstraintOS\runs\output-poc\supra_2jz_gte_twin_turbo\20260712-151228
index_html: D:\Code\ConstraintOS\runs\output-poc\supra_2jz_gte_twin_turbo\20260712-151228\index.html
manifest: D:\Code\ConstraintOS\runs\output-poc\supra_2jz_gte_twin_turbo\20260712-151228\graphic-output-manifest.json
permutations: D:\Code\ConstraintOS\runs\output-poc\supra_2jz_gte_twin_turbo\20260712-151228\graphic-output-permutations.json
validation: D:\Code\ConstraintOS\runs\output-poc\supra_2jz_gte_twin_turbo\20260712-151228\graphic-output-validation.json
review_packet: D:\Code\ConstraintOS\runs\output-poc\supra_2jz_gte_twin_turbo\20260712-151228\graphic-output-review-packet.json
final_decision: needs_review
approval_allowed: false
reported_on: 2026-07-12
assistant_ran_demo: false
```

## Out of scope until separately authorized

```text
- No unrestricted image generation.
- No production artwork generation.
- No real local image input.
- No local_file_path loading.
- No file_uri loading.
- No artifact download.
- No network fetch.
- No image decoding.
- No pixel inspection.
- No CV/OCR provider integration.
- No automatic scoring beyond deterministic fixture-safe validation.
- No automatic approval.
```

## Guardrail interpretation

This milestone may create deterministic fixture-safe output specifications or controlled placeholder artifacts. It must not claim to create production-ready generated graphics.

The output permutations are allowed to be business-visible, but they remain governed by the same trust model:

```text
requirements are source of truth
uncertainty defaults to needs_review
approval_allowed remains false
```

## Implementation phases

```text
Phase 1: contract and data model
- Define fixture-safe output permutation schema.
- Define manifest schema.
- Define validation evidence schema.
- Define review packet shape.

Phase 2: deterministic Toyota fixture data
- Add Toyota Supra A80 / 2JZ-GTE output permutation fixtures.
- Include variant intent, constraints referenced, expected risks, and review notes.

Phase 3: CLI or watch script
- Add scripts/watch-constraintos-output-poc.ps1.
- Generate output-poc run folder.
- Preserve static / fixture-safe execution only.

Phase 4: browser business demo
- Add index.html that shows constraints -> permutations -> validation -> needs_review.
- Make the output-permutation concept visible to business reviewers.

Phase 5: feedback loop
- Connect output demo feedback to the existing Toyota business demo feedback synthesis workflow.
- Collect reviewer signals about clarity, trust, product relevance, and next-step expectations.
- Preserve fixture-safe scope until feedback supports a separately gated next milestone.
```

## Phase status summary

```text
kickoff: complete
phase_1_contract_and_data_model: complete
phase_2_deterministic_toyota_fixture_data: complete
phase_3_watch_script: complete
phase_4_browser_business_demo: ready-to-show
phase_5_feedback_loop: complete
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_constraint_driven_graphic_output_permutation_poc.py
result: 9 passed
reported_on: 2026-07-12
assistant_ran_tests: false
```

## Phase 3 / Phase 4 watch-script verification record

```text
source: user-reported local test run
command: pytest tests/test_constraint_driven_graphic_output_permutation_watch_script.py
result: 9 passed
reported_on: 2026-07-12
assistant_ran_tests: false
```

## Reviewer handoff verification record

```text
source: user-reported local test run
command: pytest tests/test_constraint_driven_graphic_output_permutation_reviewer_handoff.py
result: 5 passed
reported_on: 2026-07-12
assistant_ran_tests: false
```

## Reviewer handoff rerun verification record

```text
source: user-reported local test run
command: pytest tests/test_constraint_driven_graphic_output_permutation_reviewer_handoff.py
result: 5 passed
reported_on: 2026-07-13
assistant_ran_tests: false
```

## Phase 5 feedback loop verification record

```text
source: user-reported local test run
command: pytest tests/test_constraint_driven_graphic_output_permutation_feedback_loop.py
result: 6 passed
reported_on: 2026-07-13
assistant_ran_tests: false
```

## Done criteria for this kickoff slice

```text
[x] Milestone exists.
[x] Toyota Supra use case is selected.
[x] Corrected product-shaped POC target is recorded.
[x] Fixture-safe output permutations are explicitly allowed.
[x] Production generated graphics remain out of scope.
[x] Proposed command is recorded.
[x] Proposed run-folder outputs are recorded.
[x] Implementation phases are defined.
[x] Guardrails are preserved.
[x] Verification test result recorded.
```

## Verification command

```powershell
pytest tests/test_constraint_driven_graphic_output_permutation_poc.py
pytest tests/test_constraint_driven_graphic_output_permutation_watch_script.py
pytest tests/test_constraint_driven_graphic_output_permutation_reviewer_handoff.py
pytest tests/test_constraint_driven_graphic_output_permutation_feedback_loop.py
```