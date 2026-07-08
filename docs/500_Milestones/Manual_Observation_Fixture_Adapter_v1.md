# Manual Observation Fixture Adapter v1

## Status

```text
milestone: Manual Observation Fixture Adapter v1
status: implementation-complete-pending-test
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

## Implemented files

```text
docs/500_Milestones/Manual_Observation_Fixture_Adapter_v1.md
examples/graphics/candidate_evaluation/manual_observation.schema.json
examples/graphics/candidate_evaluation/perseverance_manual_observation.fixture.json
examples/graphics/candidate_evaluation/supra_2jz_gte_manual_observation.fixture.json
src/constraintos/manual_observations.py
src/constraintos/candidate_manifests_cli.py
tests/test_manual_observation_fixture_adapter.py
examples/graphics/candidate_evaluation/README.md
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
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

## Observation boundaries

```text
- Observation mode is fixture_only.
- Source type is manual_human_review.
- Candidate image references remain reference_only_not_loaded.
- Real image ingestion is not run.
- Computer vision is not run.
- OCR is not run.
- Image generation is not run.
- Approval automation is not run.
- Recommendation remains needs_review.
- Approval remains disallowed.
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

## Done criteria

```text
[x] Manual observation fixture schema exists.
[x] Perseverance manual observation fixture exists.
[x] Supra 2JZ-GTE manual observation fixture exists.
[x] Manual observation helper module exists.
[x] CLI exposes cos-graphics-candidates observe.
[x] Text output is supported.
[x] JSON output is supported.
[x] JSON file output is supported.
[x] Command reference updated in the same implementation slice.
[ ] Verification test result recorded.
```
