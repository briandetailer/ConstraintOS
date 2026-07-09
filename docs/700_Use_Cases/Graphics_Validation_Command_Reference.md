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
- fixture-only candidate evaluation
- foundation readiness review
- observation adapter design verification
- manual observation fixture adapter
- observation-to-report binding
- fixture-only observation evidence merge
- fixture-only candidate review packet
- foundation exit review
- real candidate image intake design
- candidate image byte loading design
- candidate image byte loading contract
- candidate intake manifest contract
- candidate intake manifest discovery
- candidate intake review packet
- intake foundation exit review
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

```powershell
cos-graphics-validate perseverance --plan-only --format text
cos-graphics-validate perseverance --format text
cos-graphics-validate perseverance --format json
cos-graphics-validate perseverance --format json --output reports/perseverance-graphics-validation.json
```

## Perseverance watch mode

```powershell
cos-graphics-validate perseverance --watch
cos-graphics-validate perseverance --watch --watch-delay-ms 250
.\scripts\watch-perseverance.ps1
.\scripts\watch-perseverance.ps1 -WatchDelayMs 500
```

Generated run artifacts remain local-only by default under ignored `runs/` output.

## Reusable graphics contract validation

```powershell
pytest tests/test_graphics_contracts.py
```

## Graphics contract discovery CLI

```powershell
cos-graphics-contracts list
cos-graphics-contracts show perseverance
cos-graphics-contracts show wind_turbine_nacelle
cos-graphics-contracts show hydroelectric_dam_powerhouse
cos-graphics-contracts show supra_2jz_gte_twin_turbo
cos-graphics-contracts --format json --output reports/graphics-contracts.json list
cos-graphics-contracts --format json show supra_2jz_gte_twin_turbo
pytest tests/test_graphics_contracts_cli.py
```

## Graphics contract runtime bridge

```powershell
cos-graphics-contracts run perseverance --plan-only
cos-graphics-contracts run wind_turbine_nacelle
cos-graphics-contracts run hydroelectric_dam_powerhouse
cos-graphics-contracts run supra_2jz_gte_twin_turbo
cos-graphics-contracts --format json --output reports/supra-contract-runtime.json run supra_2jz_gte_twin_turbo
pytest tests/test_graphics_contract_runtime_bridge.py
```

## Graphics contract runtime watch mode

```powershell
cos-graphics-contracts run perseverance --plan-only --watch
cos-graphics-contracts run wind_turbine_nacelle --watch
cos-graphics-contracts run hydroelectric_dam_powerhouse --watch
cos-graphics-contracts run supra_2jz_gte_twin_turbo --watch
cos-graphics-contracts run supra_2jz_gte_twin_turbo --watch --watch-delay-ms 250
```

## Graphics contract watch capture

```powershell
.\scripts\watch-graphics-contract.ps1
.\scripts\watch-graphics-contract.ps1 -Contract supra_2jz_gte_twin_turbo
.\scripts\watch-graphics-contract.ps1 -Contract perseverance -PlanOnly
.\scripts\watch-graphics-contract.ps1 -Contract hydroelectric_dam_powerhouse -WatchDelayMs 500
pytest tests/test_graphics_contract_watch_capture_script.py
```

Generated run artifacts remain local-only by default under ignored `runs/graphics-contracts/` output.

## Candidate evaluation adapter design

```powershell
pytest tests/test_candidate_evaluation_adapter_design.py
```

This is a design-only verification command. It does not evaluate real candidate images and does not generate images.

## Candidate manifest schema

```powershell
pytest tests/test_candidate_manifest_schema.py
```

This is a schema-only verification command. It does not evaluate real candidate images and does not generate images.

## Candidate manifest discovery

```powershell
cos-graphics-candidates list
cos-graphics-candidates show perseverance
cos-graphics-candidates show supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/candidate-manifests.json list
pytest tests/test_candidate_manifest_discovery_cli.py
```

This is a read-only discovery command. It does not evaluate real candidate images and does not generate images.

## Candidate evaluation report contract

```powershell
pytest tests/test_candidate_evaluation_report_contract.py
```

This is a report-contract verification command. It does not evaluate real candidate images and does not generate images.

## Fixture-only candidate evaluation

```powershell
cos-graphics-candidates evaluate perseverance
cos-graphics-candidates evaluate supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-candidate-evaluation.json evaluate perseverance
pytest tests/test_fixture_only_candidate_evaluation.py
```

This is a fixture-only command. It loads static manifest and report fixtures, but it does not load, decode, inspect, or evaluate image bytes.

## Foundation readiness review

```powershell
pytest tests/test_foundation_readiness_review.py
```

This is a documentation and guardrail verification command. It does not evaluate real candidate images and does not generate images.

## Observation adapter design

```powershell
pytest tests/test_observation_adapter_design.py
```

This is a design-only verification command. It does not load real candidate images, choose machine-observation providers, evaluate real candidate images, or generate images.

## Manual observation fixture adapter

```powershell
cos-graphics-candidates observe perseverance
cos-graphics-candidates observe supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-observations.json observe perseverance
pytest tests/test_manual_observation_fixture_adapter.py
```

This is a fixture-only command. It loads static manifest and manual-observation fixtures, but it does not load, decode, inspect, or evaluate image bytes.

## Observation-to-report binding

```powershell
cos-graphics-candidates bind-observations perseverance
cos-graphics-candidates bind-observations supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-observation-binding.json bind-observations perseverance
pytest tests/test_observation_report_binding.py
```

This is a fixture-only command. It binds static manifest, manual-observation, and candidate-evaluation report fixtures, but it does not mutate reports, score candidates, load image bytes, or approve candidates.

## Fixture-only observation evidence merge

```powershell
cos-graphics-candidates merge-evidence perseverance
cos-graphics-candidates merge-evidence supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-merged-evidence.json merge-evidence perseverance
pytest tests/test_observation_evidence_merge.py
```

This is a fixture-only command. It produces derived merged evidence from static manual-observation and candidate-evaluation report fixtures, but it does not mutate reports, score candidates, load image bytes, or approve candidates.

## Fixture-only candidate review packet

```powershell
cos-graphics-candidates review-packet perseverance
cos-graphics-candidates review-packet supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-review-packet.json review-packet perseverance
pytest tests/test_candidate_review_packet.py
```

This is a fixture-only command. It summarizes candidate identity, manual observations, report status, merged evidence, and approval blockers, but it does not mutate reports, score candidates, load image bytes, or approve candidates.

## Foundation exit review

```powershell
pytest tests/test_foundation_exit_review.py
```

This is a documentation and guardrail verification command. It does not load real candidate images, score candidates, choose providers, or generate images.

## Real candidate image intake design

```powershell
pytest tests/test_real_candidate_image_intake_design.py
```

This is a design-only verification command. It does not load image bytes, decode images, fetch network images, inspect pixels, score candidates, choose providers, or approve candidates.

## Candidate image byte loading design

Validate future byte-loading policy boundaries before any byte loading implementation:

```powershell
pytest tests/test_candidate_image_byte_loading_design.py
```

This is a design-only verification command. It does not open files, download artifacts, fetch network resources, load image bytes, decode images, inspect pixels, score candidates, mutate reports, choose providers, or approve candidates.

## Candidate image byte loading contract

Validate the static byte-loading record schema and fixture records:

```powershell
pytest tests/test_candidate_image_byte_loading_contract.py
```

This is a contract-only verification command. It does not open files, download artifacts, fetch network resources, load image bytes, decode images, inspect pixels, score candidates, mutate reports, choose providers, or approve candidates.

## Candidate intake manifest contract

```powershell
pytest tests/test_candidate_intake_manifest_contract.py
```

This is a contract-only verification command. It does not load image bytes, decode images, fetch network images, inspect pixels, score candidates, mutate reports, or approve candidates.

## Candidate intake manifest discovery

```powershell
cos-graphics-candidates intake-list
cos-graphics-candidates intake-show perseverance
cos-graphics-candidates intake-show supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/candidate-intake-manifests.json intake-list
pytest tests/test_candidate_intake_manifest_discovery_cli.py
```

This is a read-only discovery command. It does not load image bytes, decode images, fetch network images, inspect pixels, score candidates, mutate reports, or approve candidates.

## Candidate intake review packet

Create a human-facing fixture-only intake review packet:

```powershell
cos-graphics-candidates intake-review-packet perseverance
cos-graphics-candidates intake-review-packet supra_2jz_gte_twin_turbo
```

Write a fixture-only candidate intake review packet as JSON:

```powershell
cos-graphics-candidates --format json --output reports/perseverance-intake-review-packet.json intake-review-packet perseverance
```

Run the candidate intake review packet tests:

```powershell
pytest tests/test_candidate_intake_review_packet.py
```

This is a fixture-only command. It summarizes intake candidate identity, reference metadata, policy snapshot, intake boundaries, and approval blockers, but it does not load image bytes, decode images, fetch network images, inspect pixels, score candidates, mutate reports, or approve candidates.

## Intake foundation exit review

Validate the fixture-only intake metadata foundation exit checkpoint before byte-loading design:

```powershell
pytest tests/test_intake_foundation_exit_review.py
```

This is a documentation and guardrail verification command. It does not load image bytes, decode images, fetch network images, inspect pixels, score candidates, mutate reports, choose providers, or approve candidates.

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
pytest tests/test_fixture_only_candidate_evaluation.py
pytest tests/test_foundation_readiness_review.py
pytest tests/test_observation_adapter_design.py
pytest tests/test_manual_observation_fixture_adapter.py
pytest tests/test_observation_report_binding.py
pytest tests/test_observation_evidence_merge.py
pytest tests/test_candidate_review_packet.py
pytest tests/test_foundation_exit_review.py
pytest tests/test_real_candidate_image_intake_design.py
pytest tests/test_candidate_image_byte_loading_design.py
pytest tests/test_candidate_image_byte_loading_contract.py
pytest tests/test_candidate_intake_manifest_contract.py
pytest tests/test_candidate_intake_manifest_discovery_cli.py
pytest tests/test_candidate_intake_review_packet.py
pytest tests/test_intake_foundation_exit_review.py
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

Use these keys with `cos-graphics-candidates show`, `cos-graphics-candidates evaluate`, `cos-graphics-candidates observe`, `cos-graphics-candidates bind-observations`, `cos-graphics-candidates merge-evidence`, `cos-graphics-candidates review-packet`, `cos-graphics-candidates intake-show`, and `cos-graphics-candidates intake-review-packet`:

```text
perseverance
supra_2jz_gte
supra_2jz_gte_twin_turbo
```

## Guardrails

```text
- These commands are dry-run / fixture-only / design-only / contract-only / read-only for graphics validation.
- These commands do not generate images.
- These commands do not evaluate real generated candidates yet.
- Real candidate image intake design, candidate image byte-loading design, byte-loading contract fixtures, intake manifests, and intake review packets do not load or decode images.
- Approval expectations remain contract-driven and default uncertainty to needs_review.
```
