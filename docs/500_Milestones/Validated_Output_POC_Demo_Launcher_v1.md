# Validated Output POC Demo Launcher v1

## Status

```text
milestone: Validated Output POC Demo Launcher v1
status: active
phase_1_validated_demo_launcher_status: ready-for-verification
started_on: 2026-07-15
track: Business Demo Visibility Track
previous_milestone: docs/500_Milestones/Deterministic_SVG_Structural_Validation_v1.md
launcher_script: scripts/run-validated-output-poc-demo.ps1
generator_script: scripts/watch-constraintos-output-poc.ps1
validator_script: scripts/validate-output-poc-svg-graphics.ps1
browser_helper_script: scripts/open-latest-output-poc-browser.ps1
scenario_key: supra_2jz_gte_twin_turbo
primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic
implementation_authority: deterministic-fixture-safe-validated-demo-launcher-only
assistant_ran_tests: false
assistant_ran_demo: false
```

## Purpose

Provide a single user-facing command that runs the validated output POC demo path end to end: generate deterministic output artifacts, validate SVG structural evidence, update reviewer-facing evidence artifacts, and open the generated browser UI.

```text
one command -> generate output POC -> validate SVG evidence -> update browser evidence -> open latest browser UI
```

## Product promise for this milestone

```text
- Run the fixture-safe output POC generator.
- Run the deterministic SVG structural validator.
- Open the latest output POC browser UI by default.
- Allow a NoOpenBrowser mode for terminal-only verification.
- Preserve needs_review and approval_allowed: false.
- Preserve deterministic fixture-safe scope.
```

## Target launcher command

```powershell
.\scripts\run-validated-output-poc-demo.ps1
```

## Optional terminal-only command

```powershell
.\scripts\run-validated-output-poc-demo.ps1 -NoOpenBrowser
```

## Explicitly blocked scope

```text
- Real generated final graphics.
- Production artwork generation.
- Real local image input.
- local_file_path loading.
- file_uri loading.
- Artifact download.
- Network fetch.
- Image decoding.
- Pixel inspection.
- CV/OCR provider integration.
- Automatic approval.
```

## Done criteria

```text
[x] Milestone exists.
[x] Previous deterministic SVG structural validation milestone is referenced.
[x] Launcher command is defined.
[x] Generator script dependency is defined.
[x] Validator script dependency is defined.
[x] Browser helper script dependency is defined.
[x] NoOpenBrowser mode is defined.
[x] Blocked scope is preserved.
[ ] Launcher script exists.
[ ] Verification result recorded.
```

## Verification command

```powershell
pytest tests/test_validated_output_poc_demo_launcher_milestone.py
pytest tests/test_run_validated_output_poc_demo_script.py
.\scripts\run-validated-output-poc-demo.ps1
```
