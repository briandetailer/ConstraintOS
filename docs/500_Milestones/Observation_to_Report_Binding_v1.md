# Observation-to-Report Binding v1

## Status

```text
milestone: Observation-to-Report Binding v1
status: active
started_on: 2026-07-08
previous_gate: Manual Observation Fixture Adapter v1 complete
track: Foundation Completion Track
baseline: 487 passed
```

## Purpose

Bind manual observation fixtures to fixture-only candidate evaluation reports before any real image ingestion work begins.

This milestone compares the static candidate manifest, manual observation fixture, and candidate evaluation report fixture for the same candidate. It verifies that all three artifacts agree on the candidate id, manifest id, contract key, and reference-only status, then returns a safe binding report.

## Scope

```text
- Add observation-to-report binding helper module.
- Add cos-graphics-candidates bind-observations.
- Bind candidate manifest, manual observation fixture, and candidate evaluation report fixture.
- Preserve needs_review when observations remain not observed.
- Preserve approval_allowed false.
- Support text and JSON output.
- Add tests for binding, CLI output, and guardrails.
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
- No mutation of existing report fixtures.
```

## Verification command

```powershell
pytest tests/test_observation_report_binding.py
```

## CLI commands

```powershell
cos-graphics-candidates bind-observations perseverance
cos-graphics-candidates bind-observations supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-observation-binding.json bind-observations perseverance
```

## Guardrails

```text
- Binding behavior is fixture-only.
- Candidate image references remain reference_only_not_loaded.
- Manual observations cannot approve alone.
- Evaluation reports cannot become approved from this binding.
- Recommendation remains needs_review.
- Approval remains disallowed.
- Do not claim tests passed unless actually run.
```
