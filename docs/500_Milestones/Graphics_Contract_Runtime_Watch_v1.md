# Graphics Contract Runtime Watch v1

## Status

```text
milestone: Graphics Contract Runtime Watch v1
status: active
started_on: 2026-07-08
previous_gate: Graphics Contract Runtime Bridge v1 complete
baseline: 487 passed
```

## Purpose

Add a demo-friendly watch mode for contract-backed graphics runtime bridge runs.

This milestone makes `cos-graphics-contracts run` easier to record and explain by printing a step-by-step trace of the generated runtime nodes, schedule assignments, dry-run results, and final fixture-only status.

## Scope

```text
- Add --watch to cos-graphics-contracts run.
- Add optional --watch-delay-ms for screen recording.
- Keep watch output text-only and deterministic.
- Cover plan-only and dry-run runtime bridge output.
- Update docs with watch commands.
```

## Out of scope

```text
- No image generation.
- No generated-candidate evaluation.
- No approval decision change.
- No persistent transcript script unless explicitly requested later.
```

## Implementation slices

```text
[x] Create milestone doc
[ ] Add contract runtime watch formatter
[ ] Add --watch argument
[ ] Add --watch-delay-ms argument
[ ] Add watch-output tests
[ ] Update README usage notes
[ ] Run tests and record verified result
```

## Verification commands

```powershell
pytest tests/test_graphics_contracts_cli.py
pytest tests/test_graphics_contract_runtime_bridge.py
```

## Guardrails

```text
- Keep watch output dry-run and fixture-only.
- Do not introduce image generation.
- Do not claim tests passed unless actually run.
```
