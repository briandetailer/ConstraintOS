# Graphics Contract Runtime Bridge v1

## Status

```text
milestone: Graphics Contract Runtime Bridge v1
status: active
started_on: 2026-07-08
previous_gate: Graphics Contract CLI Discovery v1 complete
baseline: 487 passed
```

## Purpose

Bridge reusable graphics-validation contracts into runtime-ready dry-run payloads.

This milestone lets a selected contract produce an in-memory runtime specification, worker list, plan, schedule, dry-run execution result, and graphics-contract runtime metadata without writing a new example fixture folder for every subject.

## Scope

```text
- Generate runtime spec from a selected graphics contract.
- Generate matching graphics-validation worker capabilities.
- Run existing RuntimeEngine dry-run against the generated spec.
- Expose the bridge through cos-graphics-contracts run.
- Support text and JSON reporting.
```

## Out of scope

```text
- No image generation.
- No generated-candidate evaluation.
- No approval decision change.
- No persistent generated spec files unless explicitly requested later.
```

## Implementation slices

```text
[x] Create milestone doc
[ ] Add contract-to-runtime spec builder
[ ] Add contract runtime worker builder
[ ] Add runtime bridge payload builder
[ ] Add cos-graphics-contracts run command
[ ] Add bridge tests
[ ] Update README usage notes
[ ] Run tests and record verified result
```

## Verification commands

```powershell
pytest tests/test_graphics_contracts.py
pytest tests/test_graphics_contracts_cli.py
pytest tests/test_graphics_contract_runtime_bridge.py
```

## Guardrails

```text
- Keep this dry-run and fixture-only.
- Do not introduce image generation.
- Do not claim tests passed unless actually run.
```
