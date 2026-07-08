# Fixture-only Candidate Evaluation v1

## Status

```text
milestone: Fixture-only Candidate Evaluation v1
status: implementation-complete-pending-test
started_on: 2026-07-08
previous_gate: Candidate Evaluation Report Contract v1 complete
track: Foundation Completion Track
baseline: 487 passed
```

## Purpose

Add the first controlled candidate evaluation behavior using static manifest and report fixtures only.

This milestone does not evaluate real candidate images. It loads an existing candidate manifest fixture, loads the matching candidate evaluation report fixture, validates the binding, and reports the fixture-only recommendation.

## Scope

```text
- Add fixture-only candidate evaluation helpers.
- Bind candidate manifests to static evaluation report fixtures.
- Add cos-graphics-candidates evaluate.
- Support text and JSON output.
- Preserve needs_review for fixture-only not-observed evidence.
- Add tests for CLI behavior, report binding, and guardrails.
- Update the candidate evaluation README.
- Update the command reference with new available commands.
```

## Out of scope

```text
- No real image loading or decoding.
- No computer-vision integration.
- No image generation.
- No image editing.
- No approval automation change.
- No approved candidate result.
- No evidence observation beyond static fixture reports.
```

## Implementation slices

```text
[x] Create milestone doc
[x] Add fixture-only candidate evaluation helpers
[x] Add cos-graphics-candidates evaluate command
[x] Add fixture-only evaluation tests
[x] Update candidate evaluation README
[x] Update command reference
[ ] Run tests and record verified result
```

## Implemented files

```text
src/constraintos/candidate_evaluation.py
src/constraintos/candidate_manifests_cli.py
tests/test_fixture_only_candidate_evaluation.py
examples/graphics/candidate_evaluation/README.md
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
```

## Verification command

```powershell
pytest tests/test_fixture_only_candidate_evaluation.py
```

## CLI commands

```powershell
cos-graphics-candidates evaluate perseverance
cos-graphics-candidates evaluate supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-candidate-evaluation.json evaluate perseverance
```

## Evaluation boundaries

```text
- Evaluation mode is fixture_only.
- Candidate image references remain reference_only_not_loaded.
- Real image ingestion is not run.
- Computer vision is not run.
- Image generation is not run.
- Approval automation is not run.
- Evidence remains not_observed.
- Recommendation remains needs_review.
- Approval remains disallowed.
```

## Guardrails

```text
- Evaluation behavior is fixture-only.
- Candidate image references remain reference_only_not_loaded.
- Real image evidence is not observed.
- Recommendation remains needs_review.
- Approval remains disallowed.
- Do not claim tests passed unless actually run.
```

## Done criteria

```text
[x] Static candidate manifests can be fixture-evaluated.
[x] Fixture-only evaluation resolves matching static report fixtures.
[x] Fixture-only evaluation validates report-to-manifest binding.
[x] CLI exposes cos-graphics-candidates evaluate.
[x] Text output is supported.
[x] JSON output is supported.
[x] JSON file output is supported.
[x] Command reference updated in the same implementation slice.
[ ] Verification test result recorded.
```
