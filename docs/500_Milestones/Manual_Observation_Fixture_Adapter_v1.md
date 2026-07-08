# Manual Observation Fixture Adapter v1

## Status

```text
milestone: Manual Observation Fixture Adapter v1
status: active
started_on: 2026-07-08
previous_gate: Observation Adapter Design v1 complete
track: Foundation Completion Track
baseline: 487 passed
```

## Purpose

Add the first fixture-only observation adapter using manually recorded observations.

This milestone does not load real candidate images. It reads static candidate manifest fixtures and matching manual observation fixtures, validates their binding, normalizes the observation summary, and returns a safe non-approval decision.

## Scope

```text
- Add manual observation fixture schema.
- Add manual observation fixtures for Perseverance and Supra 2JZ-GTE candidates.
- Add manual observation helper module.
- Add cos-graphics-candidates observe.
- Support text and JSON output.
- Preserve needs_review unless observations are complete and sufficient for a future scoring gate.
- Preserve approval_allowed false.
- Add tests for fixture loading, binding, CLI output, and guardrails.
- Update candidate evaluation README.
- Update command reference with new available commands.
```

## Out of scope

```text
- No real image loading or decoding.
- No computer-vision provider integration.
- No OCR provider integration.
- No image generation.
- No image editing.
- No automatic approval.
- No candidate-evaluation scoring behavior change.
```

## Verification command

```powershell
pytest tests/test_manual_observation_fixture_adapter.py
```

## CLI commands

```powershell
cos-graphics-candidates observe perseverance
cos-graphics-candidates observe supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-observations.json observe perseverance
```

## Guardrails

```text
- Manual observations are fixture-only.
- Candidate image references remain reference_only_not_loaded.
- Manual observations cannot approve alone.
- Observation summary defaults to needs_review.
- Approval remains disallowed.
- Do not claim tests passed unless actually run.
```
