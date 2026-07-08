# Graphics Contract Watch Capture v1

## Status

```text
milestone: Graphics Contract Watch Capture v1
status: complete
started_on: 2026-07-08
completed_on: 2026-07-08
previous_gate: Graphics Contract Runtime Watch v1 complete
baseline: 487 passed
latest_user_reported_capture_script_test_result: 5 passed
latest_user_reported_capture_script_test_result_on: 2026-07-08
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
[x] Add graphics contract watch capture script
[x] Add script coverage tests
[x] Update graphics command reference
[x] Run tests and record verified result
```

## Implemented files

```text
scripts/watch-graphics-contract.ps1
tests/test_graphics_contract_watch_capture_script.py
docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
```

## Verification command

```powershell
pytest tests/test_graphics_contract_watch_capture_script.py
```

## Verification record

```text
source: user-reported local test run
command: pytest tests/test_graphics_contract_watch_capture_script.py
platform: win32
python: 3.12.10
pytest: 9.1.1
result: 5 passed in 0.18s
reported_on: 2026-07-08
assistant_ran_tests: false
```

## CLI commands

```powershell
.\scripts\watch-graphics-contract.ps1
.\scripts\watch-graphics-contract.ps1 -Contract supra_2jz_gte_twin_turbo
.\scripts\watch-graphics-contract.ps1 -Contract perseverance -PlanOnly
.\scripts\watch-graphics-contract.ps1 -Contract hydroelectric_dam_powerhouse -WatchDelayMs 500
```

## Local output files

```text
runs/graphics-contracts/<contract>/<timestamp>/terminal-transcript.txt
runs/graphics-contracts/<contract>/<timestamp>/watch-output.txt
runs/graphics-contracts/<contract>/<timestamp>/graphics-contract-runtime-result.json
runs/graphics-contracts/<contract>/<timestamp>/run-metadata.json
```

## Guardrails

```text
- Capture outputs must remain local under ignored runs/ paths.
- Keep the script dry-run / fixture-only.
- Do not introduce image generation.
- Do not claim tests passed unless actually run.
```

## Done criteria

```text
[x] Capture helper exists for any graphics contract key.
[x] Capture helper supports dry-run capture.
[x] Capture helper supports plan-only capture.
[x] Capture helper writes transcript, watch output, JSON result, and metadata.
[x] Command reference updated in the same implementation slice.
[x] Verification test result recorded.
```

## Handoff notes

```text
- Graphics Contract Watch Capture v1 is complete.
- Contract-backed watch runs can now be captured locally with transcript, watch output, JSON runtime report, and metadata.
- Captured output remains local-only under ignored runs/graphics-contracts/ paths.
- The command reference was updated in the same implementation slice.
- The next milestone should begin candidate-evaluation adapter design while keeping image generation gated, or add a higher-level demo runbook that links the command reference, contracts, and captured outputs.
```
