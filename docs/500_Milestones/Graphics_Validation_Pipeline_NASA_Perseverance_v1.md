# Graphics Validation Pipeline - NASA Perseverance v1

## Status

```text
milestone: Graphics Validation Pipeline - NASA Perseverance v1
status: implementation-complete-pending-wrapper-test
started_on: 2026-07-07
previous_gate: Runtime Package Artifact Handoff complete
baseline: 487 passed
latest_user_reported_test_result: 4 passed
latest_user_reported_test_result_on: 2026-07-07
```

## Purpose

Turn the documented NASA Perseverance rover graphics use case into executable ConstraintOS runtime inputs and expected validation outputs.

This milestone starts the product-facing graphics validation path. It does not generate final images yet. It builds the pipeline around one documented use case so ConstraintOS can define what a valid generated graphic must preserve before an image model is introduced.

## Source use case

```text
docs/700_Use_Cases/Use_Case_1_NASA_Perseverance_Rover_Technical_Graphic.md
```

## Validation target

```text
subject: NASA Perseverance rover
view: front-left three-quarter view
style: clean engineering-manual technical infographic
label_density: full instrument labels plus major subsystem labels
output_format: landscape poster
```

## Core question

```text
Can ConstraintOS preserve a complex, real-world engineering subject across style, view, label-density, and output-format permutations while rejecting plausible-looking but incorrect graphics?
```

## Implementation slices

```text
[x] Create milestone doc for Graphics Validation Pipeline - NASA Perseverance v1
[x] Create example spec.json for Use Case 1
[x] Create example workers.json for graphics-validation workflow roles
[x] Create example policy.json for subject / geometry / label / evidence rules
[x] Create expected prompt output fixture
[x] Create expected evidence report fixture
[x] Create expected approval result fixture
[x] Add runtime fixture tests for the Perseverance example
[x] Document example runtime commands
[x] Run tests and record verified result
[x] Add first graphics-validation CLI/API wrapper around the example
[ ] Run graphics-validation wrapper tests and record verified result
```

## Example fixture paths

```text
examples/graphics/perseverance/README.md
examples/graphics/perseverance/spec.json
examples/graphics/perseverance/workers.json
examples/graphics/perseverance/policy.json
examples/graphics/perseverance/expected_prompt.json
examples/graphics/perseverance/expected_evidence.json
examples/graphics/perseverance/expected_approval.json
runtime/tests/test_graphics_perseverance_example.py
```

## Graphics-validation wrapper paths

```text
src/constraintos/graphics_validation_cli.py
tests/test_graphics_validation_cli.py
pyproject.toml project script: cos-graphics-validate
```

## Runtime approach

```text
- Use the existing Runtime Planner, Scheduler, and DryRunExecutor.
- Model graphics validation as a multi-node runtime plan.
- Preserve the future product workflow while keeping current execution deterministic.
- Use expected fixtures for prompt, evidence, and approval outputs until image generation/evaluation adapters exist.
```

## Pipeline stages

```text
1. collect_references
2. build_constraints
3. generate_prompt
4. evaluate_candidate
5. build_evidence
6. review_approval
```

## Required graphics constraints

```text
subject_identity:
- Must remain NASA Perseverance rover.
- Must not become Curiosity, Opportunity, Spirit, a generic rover, a lunar rover, or a fictional rover.

geometry:
- Six wheels must remain visible or logically present.
- Wheel layout must follow rocker-bogie rover geometry.
- Mast must rise from the rover body.
- Robotic arm must attach to the front/body area.
- Instrument turret must be at the end of the robotic arm.

instrument_labeling:
- Mastcam-Z and SuperCam must be associated with the mast/camera head.
- PIXL and SHERLOC must be associated with the arm/turret region.
- MOXIE must be treated as an internal/body-mounted payload.
- RIMFAX must be associated with the lower/rear underside antenna region.
- MEDA must be represented as environmental sensors.

approval_behavior:
- Missing, ambiguous, or incorrectly placed required subsystems must mark the output needs_review.
- Plausible-looking but mechanically/subject-incorrect images must not be approved.
```

## Verification policy

```text
- Do not claim local tests passed unless actually run.
- Keep the user-confirmed baseline explicit: 487 passed.
- Do not reopen Runtime Milestone 3.
- Keep image generation out of this milestone until the pipeline and expected evidence shape are established.
```

## Manual verification commands

```bash
cos-graphics-validate perseverance --plan-only --format text

cos-graphics-validate perseverance --format text

pytest runtime/tests/test_graphics_perseverance_example.py
pytest tests/test_graphics_validation_cli.py
```

## Verification record

```text
source: user-reported local test run
command: pytest runtime/tests/test_graphics_perseverance_example.py
result: 4 passed
reported_on: 2026-07-07
assistant_ran_tests: false
```

## Wrapper behavior

```text
- Defaults to the Perseverance graphics-validation fixture.
- Reuses the existing Runtime Planner, Scheduler, and DryRunExecutor.
- Supports plan-only and dry-run runtime execution.
- Emits graphics_validation metadata in JSON output.
- Appends graphics-validation subject, expected decision, and mode to text output.
- Keeps expected decision at needs_review while candidate image generation remains fixture-only.
```

## Done criteria

```text
[x] Fixture files exist and are internally consistent.
[x] Runtime dry-run can schedule and execute all graphics-validation nodes using the example workers.
[x] Tests confirm required labels, forbidden substitutions, and needs_review behavior are represented.
[x] First CLI/API wrapper is identified as the next implementation slice.
[ ] Wrapper tests confirm plan-only JSON, runtime text output, output-file behavior, and unknown-example error handling.
```
