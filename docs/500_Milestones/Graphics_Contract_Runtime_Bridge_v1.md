# Graphics Contract Runtime Bridge v1

## Status

```text
milestone: Graphics Contract Runtime Bridge v1
status: complete
started_on: 2026-07-08
completed_on: 2026-07-08
previous_gate: Graphics Contract CLI Discovery v1 complete
baseline: 487 passed
latest_user_reported_contract_test_result: 19 passed
latest_user_reported_contract_test_result_on: 2026-07-08
latest_user_reported_cli_test_result: 6 passed
latest_user_reported_cli_test_result_on: 2026-07-08
latest_user_reported_bridge_test_result: 6 passed
latest_user_reported_bridge_test_result_on: 2026-07-08
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
[x] Add contract-to-runtime spec builder
[x] Add contract runtime worker builder
[x] Add runtime bridge payload builder
[x] Add cos-graphics-contracts run command
[x] Add bridge tests
[x] Update README usage notes
[x] Run tests and record verified result
```

## Implemented files

```text
src/constraintos/graphics_contract_runtime.py
src/constraintos/graphics_contracts_cli.py
tests/test_graphics_contract_runtime_bridge.py
examples/graphics/contracts/README.md
```

## Verification commands

```powershell
pytest tests/test_graphics_contracts.py
pytest tests/test_graphics_contracts_cli.py
pytest tests/test_graphics_contract_runtime_bridge.py
```

## Verification records

```text
source: user-reported local test run
command: pytest tests/test_graphics_contracts.py
platform: win32
python: 3.12.10
pytest: 9.1.1
result: 19 passed in 0.29s
reported_on: 2026-07-08
assistant_ran_tests: false
```

```text
source: user-reported local test run
command: pytest tests/test_graphics_contracts_cli.py
platform: win32
python: 3.12.10
pytest: 9.1.1
result: 6 passed in 0.58s
reported_on: 2026-07-08
assistant_ran_tests: false
```

```text
source: user-reported local test run
command: pytest tests/test_graphics_contract_runtime_bridge.py
platform: win32
python: 3.12.10
pytest: 9.1.1
result: 6 passed in 0.47s
reported_on: 2026-07-08
assistant_ran_tests: false
```

## CLI commands

```powershell
cos-graphics-contracts run perseverance --plan-only
cos-graphics-contracts run wind_turbine_nacelle
cos-graphics-contracts run hydroelectric_dam_powerhouse
cos-graphics-contracts run supra_2jz_gte_twin_turbo
cos-graphics-contracts --format json --output reports/supra-contract-runtime.json run supra_2jz_gte_twin_turbo
```

## Guardrails

```text
- Keep this dry-run and fixture-only.
- Do not introduce image generation.
- Do not claim tests passed unless actually run.
```

## Done criteria

```text
[x] A contract can be converted to a runtime-ready spec in memory.
[x] Generated workers cover all graphics-validation runtime plugins.
[x] Contract-backed runtime bridge can plan and schedule all six nodes.
[x] Contract-backed runtime bridge can execute dry-run runtime nodes.
[x] CLI exposes contract runtime bridge reporting.
[x] Verification test result recorded.
```

## Handoff notes

```text
- Graphics Contract Runtime Bridge v1 is complete.
- Four reusable graphics contracts can now be bridged into runtime-ready dry-run payloads.
- The bridge remains fixture-only and does not generate images.
- The next milestone should add demo-friendly watch/reporting for contract runtime runs or begin designing candidate-evaluation adapters while keeping image generation gated.
```
