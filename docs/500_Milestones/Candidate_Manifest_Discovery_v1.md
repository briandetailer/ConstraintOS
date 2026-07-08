# Candidate Manifest Discovery v1

## Status

```text
milestone: Candidate Manifest Discovery v1
status: active
started_on: 2026-07-08
previous_gate: Candidate Manifest Schema v1 complete
track: Foundation Completion Track
baseline: 487 passed
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
[ ] Add candidate manifest discovery helpers
[ ] Add cos-graphics-candidates CLI
[ ] Add package entry point
[ ] Add discovery and CLI tests
[ ] Update candidate evaluation README
[ ] Update command reference
[ ] Run tests and record verified result
```

## Verification command

```powershell
pytest tests/test_candidate_manifest_discovery_cli.py
```

## Planned commands

```powershell
cos-graphics-candidates list
cos-graphics-candidates show perseverance
cos-graphics-candidates show supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/candidate-manifests.json list
```

## Guardrails

```text
- CLI is read-only.
- CLI must report evaluation_status as not_evaluated.
- CLI must report image_generation as not run.
- CLI must not load candidate image bytes.
- Do not claim tests passed unless actually run.
```
