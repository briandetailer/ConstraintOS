# Graphics Contract Runtime Watch v1

## Status

```text
milestone: Graphics Contract Runtime Watch v1
status: implementation-complete-pending-test
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
[x] Add contract runtime watch formatter
[x] Add --watch argument
[x] Add --watch-delay-ms argument
[x] Add watch-output tests
[x] Update README usage notes
[ ] Run tests and record verified result
```

## Implemented files

```text
src/constraintos/graphics_contracts_cli.py
tests/test_graphics_contract_runtime_bridge.py
examples/graphics/contracts/README.md
```

## Verification commands

```powershell
pytest tests/test_graphics_contracts_cli.py
pytest tests/test_graphics_contract_runtime_bridge.py
```

## CLI commands

```powershell
cos-graphics-contracts run perseverance --plan-only --watch
cos-graphics-contracts run wind_turbine_nacelle --watch
cos-graphics-contracts run hydroelectric_dam_powerhouse --watch
cos-graphics-contracts run supra_2jz_gte_twin_turbo --watch
cos-graphics-contracts run supra_2jz_gte_twin_turbo --watch --watch-delay-ms 250
```

## Guardrails

```text
- Keep watch output dry-run and fixture-only.
- Do not introduce image generation.
- Do not claim tests passed unless actually run.
```

## Done criteria

```text
[x] Watch output shows contract key, subject, mode, expected decision, and image-generation status.
[x] Watch output lists all generated runtime nodes in order.
[x] Plan-only watch output marks node results as not_run_plan_only.
[x] Dry-run watch output marks node results as dry_run_complete.
[x] CLI supports optional watch delay for screen recording.
[ ] Verification test result recorded.
```
