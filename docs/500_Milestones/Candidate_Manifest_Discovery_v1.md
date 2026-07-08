# Candidate Manifest Discovery v1

## Status

```text
milestone: Candidate Manifest Discovery v1
status: complete
started_on: 2026-07-08
completed_on: 2026-07-08
previous_gate: Candidate Manifest Schema v1 complete
track: Foundation Completion Track
baseline: 487 passed
latest_user_reported_candidate_manifest_discovery_test_result: 8 passed
latest_user_reported_candidate_manifest_discovery_test_result_on: 2026-07-08
```

## Purpose

Add read-only discovery and reporting for static candidate manifest fixtures.

This milestone lets users list candidate manifests and show a selected manifest summary without evaluating real candidate images.

## Scope

```text
- Add candidate manifest discovery helpers.
- Add a read-only cos-graphics-candidates CLI.
- Support list and show commands.
- Support text and JSON output.
- Add tests for discovery, reporting, and guardrails.
- Update the candidate evaluation README.
- Update the command reference with new available commands.
```

## Out of scope

```text
- No candidate evaluation.
- No real image loading or decoding.
- No computer-vision integration.
- No image generation.
- No image editing.
- No approval automation change.
```

## Implementation slices

```text
[x] Create milestone doc
[x] Add candidate manifest discovery helpers
[x] Add cos-graphics-candidates CLI
[x] Add package entry point
[x] Add discovery and CLI tests
[x] Update candidate evaluation README
[x] Update command reference
[x] Run tests and record verified result
```

## Implemented files

```text
src/constraintos/candidate_manifests.py
src/constraintos/candidate_manifests_cli.py
pyproject.toml
tests/test_candidate_manifest_discovery_cli.py
examples/graphics/candidate_evaluation/README.md
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
```

## Verification command

```powershell
pytest tests/test_candidate_manifest_discovery_cli.py
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_candidate_manifest_discovery_cli.py
result: 8 passed
reported_on: 2026-07-08
assistant_ran_tests: false
```

## CLI commands

```powershell
cos-graphics-candidates list
cos-graphics-candidates show perseverance
cos-graphics-candidates show supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/candidate-manifests.json list
```

## Guardrails

```text
- CLI is read-only.
- CLI reports evaluation_status as not_evaluated.
- CLI reports image_generation as not run.
- CLI reports candidate_evaluation as not run.
- CLI does not load candidate image bytes.
- Do not claim tests passed unless actually run.
```

## Done criteria

```text
[x] Static candidate manifests can be listed.
[x] Static candidate manifests can be shown by manifest key.
[x] Static candidate manifests can be shown by bound contract key.
[x] JSON output is supported.
[x] Package exposes cos-graphics-candidates.
[x] Command reference updated in the same implementation slice.
[x] Verification test result recorded.
```

## Handoff notes

```text
- Candidate Manifest Discovery v1 is complete.
- Static candidate manifests can now be listed and shown through cos-graphics-candidates.
- Discovery remains read-only and does not evaluate, load, decode, inspect, or generate candidate images.
- This remains part of the Foundation Completion Track.
- The next milestone should define the fixture-only candidate evaluation report contract before implementing candidate evaluation behavior.
```
