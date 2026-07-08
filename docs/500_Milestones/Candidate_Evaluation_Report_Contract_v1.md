# Candidate Evaluation Report Contract v1

## Status

```text
milestone: Candidate Evaluation Report Contract v1
status: active
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
[ ] Add candidate evaluation report schema
[ ] Add static report fixtures
[ ] Add report schema and guardrail tests
[ ] Update candidate evaluation README
[ ] Update command reference
[ ] Run tests and record verified result
```

## Verification command

```powershell
pytest tests/test_candidate_evaluation_report_contract.py
```

## Guardrails

```text
- Reports are fixture-only.
- Reports must not claim real image evidence was observed.
- Reports must not claim image generation, image loading, or candidate evaluation ran.
- Not-observed evidence must recommend needs_review.
- Do not claim tests passed unless actually run.
```
