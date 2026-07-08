# Graphics Contract CLI Discovery v1

## Status

```text
milestone: Graphics Contract CLI Discovery v1
status: active
started_on: 2026-07-08
previous_gate: Additional Graphics Contract Instances v1 complete
baseline: 487 passed
```

## Purpose

Expose reusable graphics-validation contracts through a command-line discovery and reporting path.

This milestone lets a user list available graphics contracts and inspect a selected contract without opening JSON files directly.

## Scope

```text
- Add cos-graphics-contracts CLI.
- Support list reporting.
- Support show reporting for one contract.
- Support text and JSON output.
- Validate contracts against the shared schema during discovery.
```

## Out of scope

```text
- No image generation.
- No generated-candidate evaluation.
- No runtime execution changes.
- No approval decision changes.
```

## Implementation slices

```text
[x] Create milestone doc
[ ] Add reusable contract discovery helpers
[ ] Add cos-graphics-contracts CLI
[ ] Add package entry point
[ ] Add CLI tests for list output
[ ] Add CLI tests for show output
[ ] Add README usage notes
[ ] Run tests and record verified result
```

## Verification commands

```powershell
pytest tests/test_graphics_contracts.py
pytest tests/test_graphics_contracts_cli.py
```

## Guardrails

```text
- Keep this read-only and fixture-only.
- Do not introduce image generation.
- Do not claim tests passed unless actually run.
```
