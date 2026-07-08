# Fixture-only Candidate Evaluation v1

## Status

```text
milestone: Fixture-only Candidate Evaluation v1
status: active
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
[ ] Add fixture-only candidate evaluation helpers
[ ] Add cos-graphics-candidates evaluate command
[ ] Add fixture-only evaluation tests
[ ] Update candidate evaluation README
[ ] Update command reference
[ ] Run tests and record verified result
```

## Verification command

```powershell
pytest tests/test_fixture_only_candidate_evaluation.py
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
