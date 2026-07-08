# Graphics Contract CLI Discovery v1

## Status

```text
milestone: Graphics Contract CLI Discovery v1
status: complete
started_on: 2026-07-08
completed_on: 2026-07-08
previous_gate: Additional Graphics Contract Instances v1 complete
baseline: 487 passed
latest_user_reported_contract_test_result: 19 passed
latest_user_reported_contract_test_result_on: 2026-07-08
latest_user_reported_cli_test_result: 6 passed
latest_user_reported_cli_test_result_on: 2026-07-08
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
[x] Add reusable contract discovery helpers
[x] Add cos-graphics-contracts CLI
[x] Add package entry point
[x] Add CLI tests for list output
[x] Add CLI tests for show output
[x] Add README usage notes
[x] Run tests and record verified result
```

## Implemented files

```text
src/constraintos/graphics_contracts.py
src/constraintos/graphics_contracts_cli.py
pyproject.toml
tests/test_graphics_contracts_cli.py
examples/graphics/contracts/README.md
```

## Verification commands

```powershell
pytest tests/test_graphics_contracts.py
pytest tests/test_graphics_contracts_cli.py
```

## Verification records

```text
source: user-reported local test run
command: pytest tests/test_graphics_contracts.py
platform: win32
python: 3.12.10
pytest: 9.1.1
result: 19 passed in 0.31s
reported_on: 2026-07-08
assistant_ran_tests: false
```

```text
source: user-reported local test run after assertion patch
commands:
- git pull --rebase origin phase-1-cli-tooling
- pytest tests/test_graphics_contracts_cli.py
platform: win32
python: 3.12.10
pytest: 9.1.1
result: 6 passed in 0.33s
reported_on: 2026-07-08
assistant_ran_tests: false
```

## CLI commands

```powershell
cos-graphics-contracts list
cos-graphics-contracts show perseverance
cos-graphics-contracts show wind_turbine_nacelle
cos-graphics-contracts show hydroelectric_dam_powerhouse
cos-graphics-contracts show supra_2jz_gte_twin_turbo
cos-graphics-contracts --format json --output reports/graphics-contracts.json list
```

## Guardrails

```text
- Keep this read-only and fixture-only.
- Do not introduce image generation.
- Do not claim tests passed unless actually run.
```

## Handoff notes

```text
- Graphics Contract CLI Discovery v1 is complete.
- Four graphics-validation contracts are discoverable through cos-graphics-contracts.
- The CLI remains read-only and fixture-only.
- The next milestone should decide whether to add contract-backed runtime example generation, richer reports, or a demo-friendly contract listing/watch workflow before image generation.
```
