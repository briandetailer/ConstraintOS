# Graphics Validation Command Reference

## Purpose

This document gathers the commands introduced across the recent graphics-validation milestones.

It covers:

```text
- Perseverance graphics-validation fixture runs
- Perseverance watch-mode capture
- reusable graphics contract tests
- graphics contract discovery
- graphics contract runtime bridge runs
- graphics contract runtime watch runs
- graphics contract watch capture
- candidate evaluation adapter design verification
- candidate manifest schema verification
- candidate manifest discovery
- candidate evaluation report contract verification
- local verification commands
```

## Maintenance rule

Whenever a future milestone, script, CLI entry point, or workflow makes new user-facing commands available, update this document in the same implementation slice.

Include:

```text
- the exact command
- what the command does
- whether it is plan-only, dry-run, fixture-only, or writes files
- any relevant output path
- any related verification command
```

## Branch sync

Use this before running newly added commands locally:

```powershell
git pull --rebase origin phase-1-cli-tooling
```

## Perseverance graphics-validation fixture

Plan the Perseverance graphics-validation runtime fixture without executing it:

```powershell
cos-graphics-validate perseverance --plan-only --format text
```

Run the Perseverance graphics-validation fixture through the current dry-run runtime:

```powershell
cos-graphics-validate perseverance --format text
```

Run the Perseverance fixture and emit JSON:

```powershell
cos-graphics-validate perseverance --format json
```

Write a Perseverance graphics-validation result to a file:

```powershell
cos-graphics-validate perseverance --format json --output reports/perseverance-graphics-validation.json
```

## Perseverance watch mode

Run the Perseverance graphics-validation fixture in watch mode:

```powershell
cos-graphics-validate perseverance --watch
```

Run watch mode with a screen-recording delay:

```powershell
cos-graphics-validate perseverance --watch --watch-delay-ms 250
```

Run the PowerShell watch helper:

```powershell
.\scripts\watch-perseverance.ps1
```

Run the PowerShell watch helper with a slower delay:

```powershell
.\scripts\watch-perseverance.ps1 -WatchDelayMs 500
```

The PowerShell helper writes local run artifacts such as:

```text
terminal-transcript.txt
watch-output.txt
graphics-validation-result.json
run-metadata.json
```

Generated run artifacts remain local-only by default under ignored `runs/` output.

## Reusable graphics contract validation

Run the reusable graphics contract test suite:

```powershell
pytest tests/test_graphics_contracts.py
```

This validates the reusable graphics contract schema and the current contract instances.

## Graphics contract discovery CLI

List available graphics contracts:

```powershell
cos-graphics-contracts list
```

Show individual contract summaries:

```powershell
cos-graphics-contracts show perseverance
cos-graphics-contracts show wind_turbine_nacelle
cos-graphics-contracts show hydroelectric_dam_powerhouse
cos-graphics-contracts show supra_2jz_gte_twin_turbo
```

Write a JSON list of all graphics contracts:

```powershell
cos-graphics-contracts --format json --output reports/graphics-contracts.json list
```

Show a contract summary as JSON:

```powershell
cos-graphics-contracts --format json show supra_2jz_gte_twin_turbo
```

Run the contract discovery CLI tests:

```powershell
pytest tests/test_graphics_contracts_cli.py
```

## Graphics contract runtime bridge

Run a contract-backed runtime bridge in plan-only mode:

```powershell
cos-graphics-contracts run perseverance --plan-only
```

Run contract-backed dry-run runtime bridges:

```powershell
cos-graphics-contracts run wind_turbine_nacelle
cos-graphics-contracts run hydroelectric_dam_powerhouse
cos-graphics-contracts run supra_2jz_gte_twin_turbo
```

Write a contract runtime bridge report as JSON:

```powershell
cos-graphics-contracts --format json --output reports/supra-contract-runtime.json run supra_2jz_gte_twin_turbo
```

Run the contract runtime bridge tests:

```powershell
pytest tests/test_graphics_contract_runtime_bridge.py
```

## Graphics contract runtime watch mode

Run a plan-only contract runtime watch:

```powershell
cos-graphics-contracts run perseverance --plan-only --watch
```

Run contract-backed dry-run runtime watches:

```powershell
cos-graphics-contracts run wind_turbine_nacelle --watch
cos-graphics-contracts run hydroelectric_dam_powerhouse --watch
cos-graphics-contracts run supra_2jz_gte_twin_turbo --watch
```

Run watch mode with a screen-recording delay:

```powershell
cos-graphics-contracts run supra_2jz_gte_twin_turbo --watch --watch-delay-ms 250
```

## Graphics contract watch capture

Capture a contract-backed runtime watch with the default `perseverance` contract:

```powershell
.\scripts\watch-graphics-contract.ps1
```

Capture a specific contract-backed dry-run watch:

```powershell
.\scripts\watch-graphics-contract.ps1 -Contract supra_2jz_gte_twin_turbo
```

Capture a plan-only contract watch:

```powershell
.\scripts\watch-graphics-contract.ps1 -Contract perseverance -PlanOnly
```

Capture with a slower screen-recording delay:

```powershell
.\scripts\watch-graphics-contract.ps1 -Contract hydroelectric_dam_powerhouse -WatchDelayMs 500
```

The contract watch capture helper writes local run artifacts such as:

```text
terminal-transcript.txt
watch-output.txt
graphics-contract-runtime-result.json
run-metadata.json
```

Generated run artifacts remain local-only by default under ignored `runs/graphics-contracts/` output.

Run the contract watch capture script tests:

```powershell
pytest tests/test_graphics_contract_watch_capture_script.py
```

## Candidate evaluation adapter design

Validate the candidate evaluation adapter design fixture and guardrails:

```powershell
pytest tests/test_candidate_evaluation_adapter_design.py
```

This is a design-only verification command. It does not evaluate real candidate images and does not generate images.

## Candidate manifest schema

Validate the candidate manifest schema and static fixtures:

```powershell
pytest tests/test_candidate_manifest_schema.py
```

This is a schema-only verification command. It does not evaluate real candidate images and does not generate images.

## Candidate manifest discovery

List available static candidate manifests:

```powershell
cos-graphics-candidates list
```

Show individual candidate manifest summaries:

```powershell
cos-graphics-candidates show perseverance
cos-graphics-candidates show supra_2jz_gte_twin_turbo
```

Write a JSON report of static candidate manifests:

```powershell
cos-graphics-candidates --format json --output reports/candidate-manifests.json list
```

Run the candidate manifest discovery CLI tests:

```powershell
pytest tests/test_candidate_manifest_discovery_cli.py
```

This is a read-only discovery command. It does not evaluate real candidate images and does not generate images.

## Candidate evaluation report contract

Validate the fixture-only candidate evaluation report contract and static report fixtures:

```powershell
pytest tests/test_candidate_evaluation_report_contract.py
```

This is a report-contract verification command. It does not evaluate real candidate images and does not generate images.

## Full recent graphics-validation verification set

Run all recent graphics-validation and contract-focused test suites:

```powershell
pytest runtime/tests/test_graphics_perseverance_example.py
pytest tests/test_graphics_validation_cli.py
pytest tests/test_graphics_contracts.py
pytest tests/test_graphics_contracts_cli.py
pytest tests/test_graphics_contract_runtime_bridge.py
pytest tests/test_graphics_contract_watch_capture_script.py
pytest tests/test_candidate_evaluation_adapter_design.py
pytest tests/test_candidate_manifest_schema.py
pytest tests/test_candidate_manifest_discovery_cli.py
pytest tests/test_candidate_evaluation_report_contract.py
```

## Current contract keys

Use these keys with `cos-graphics-contracts show`, `cos-graphics-contracts run`, and `scripts/watch-graphics-contract.ps1 -Contract`:

```text
perseverance
wind_turbine_nacelle
hydroelectric_dam_powerhouse
supra_2jz_gte_twin_turbo
```

## Current candidate manifest keys

Use these keys with `cos-graphics-candidates show`:

```text
perseverance
supra_2jz_gte
supra_2jz_gte_twin_turbo
```

## Guardrails

```text
- These commands are dry-run / fixture-only for graphics validation.
- These commands do not generate images.
- These commands do not evaluate real generated candidates yet.
- Approval expectations remain contract-driven and default uncertainty to needs_review.
```
