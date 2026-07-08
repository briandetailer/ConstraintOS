# Graphics Contract Watch Capture v1

## Status

```text
milestone: Graphics Contract Watch Capture v1
status: active
started_on: 2026-07-08
previous_gate: Graphics Contract Runtime Watch v1 complete
baseline: 487 passed
```

## Purpose

Add a reusable local capture script for contract-backed graphics runtime watch runs.

This milestone captures demo-friendly watch output, JSON runtime report, terminal transcript, and run metadata for any reusable graphics contract.

## Scope

```text
- Add scripts/watch-graphics-contract.ps1.
- Support a selected contract key.
- Support dry-run and plan-only capture.
- Capture terminal transcript, watch output, JSON report, and metadata.
- Write output under ignored local runs/graphics-contracts/.
- Update the command reference with the new available commands.
```

## Out of scope

```text
- No image generation.
- No generated-candidate evaluation.
- No committed run artifacts.
- No CI workflow changes.
```

## Implementation slices

```text
[x] Create milestone doc
[ ] Add graphics contract watch capture script
[ ] Add script coverage tests
[ ] Update graphics command reference
[ ] Run tests and record verified result
```

## Verification command

```powershell
pytest tests/test_graphics_contract_watch_capture_script.py
```

## Guardrails

```text
- Capture outputs must remain local under ignored runs/ paths.
- Keep the script dry-run / fixture-only.
- Do not introduce image generation.
- Do not claim tests passed unless actually run.
```
