# Candidate Evaluation Report Contract v1

## Status

```text
milestone: Candidate Evaluation Report Contract v1
status: implementation-complete-pending-test
started_on: 2026-07-08
previous_gate: Candidate Manifest Discovery v1 complete
track: Foundation Completion Track
baseline: 487 passed
```

## Purpose

Define the fixture-only report contract for future candidate graphics evaluation.

This milestone defines what an evaluation report must look like before any candidate evaluation behavior is implemented.

## Scope

```text
- Add a candidate evaluation report JSON Schema.
- Add static report fixtures for existing candidate manifest fixtures.
- Bind reports to candidate manifests and graphics contract keys.
- Define evidence item shape, constraint status values, and recommendation shape.
- Preserve no image generation, no image editing, no image loading, and no computer-vision integration.
- Preserve needs_review as the safe default for not-observed evidence.
- Add schema and guardrail tests.
- Update the candidate evaluation README.
- Update the command reference with new verification commands.
```

## Out of scope

```text
- No candidate-evaluation CLI command.
- No real image loading or decoding.
- No computer-vision integration.
- No image generation.
- No image editing.
- No approval automation change.
- No approved candidate result.
```

## Implementation slices

```text
[x] Create milestone doc
[x] Add candidate evaluation report schema
[x] Add static report fixtures
[x] Add report schema and guardrail tests
[x] Update candidate evaluation README
[x] Update command reference
[ ] Run tests and record verified result
```

## Implemented files

```text
examples/graphics/candidate_evaluation/candidate_evaluation_report.schema.json
examples/graphics/candidate_evaluation/perseverance_candidate_evaluation_report.fixture.json
examples/graphics/candidate_evaluation/supra_2jz_gte_candidate_evaluation_report.fixture.json
tests/test_candidate_evaluation_report_contract.py
examples/graphics/candidate_evaluation/README.md
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
```

## Verification command

```powershell
pytest tests/test_candidate_evaluation_report_contract.py
```

## Report boundaries

```text
- Report status is fixture_only.
- Report mode is contract_shape_only_no_image_evaluation.
- Candidate reference status is reference_only_not_loaded.
- Candidate evaluation has not run.
- Image generation has not run.
- Image loading has not run.
- Evidence status is not_observed.
- Recommended decision is needs_review.
- Approval is not allowed.
```

## Guardrails

```text
- Reports are fixture-only.
- Reports must not claim real image evidence was observed.
- Reports must not claim image generation, image loading, or candidate evaluation ran.
- Not-observed evidence must recommend needs_review.
- Do not claim tests passed unless actually run.
```

## Done criteria

```text
[x] Candidate evaluation report JSON Schema exists.
[x] Static Perseverance candidate evaluation report fixture exists.
[x] Static Supra 2JZ-GTE candidate evaluation report fixture exists.
[x] Fixtures bind to candidate manifest fixtures.
[x] Fixtures validate against the schema.
[x] Tests reject candidate evaluation claims.
[x] Tests reject approved recommendations.
[x] Command reference updated in the same implementation slice.
[ ] Verification test result recorded.
```
