# Graphics Validation Command Reference

## Purpose

This document gathers user-facing commands and local verification commands introduced across the graphics-validation milestones.

## Maintenance rule

Whenever a future milestone, script, CLI entry point, or workflow makes new user-facing commands available, update this document in the same implementation slice.

Include:

```text
- the exact command
- what the command does
- whether it is plan-only, dry-run, fixture-only, helper-only, contract-only, read-only, or writes files
- any relevant output path
- any related verification command
```

## Branch sync

```powershell
git pull --rebase origin phase-1-cli-tooling
```

## Business demo watch commands

### End-to-end fixture POC demo

Run the full fixture-based POC demo as a visible staged product walkthrough:

```powershell
.\scripts\watch-constraintos-poc.ps1
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance
.\scripts\watch-constraintos-poc.ps1 -Scenario supra_2jz_gte_twin_turbo -WatchDelayMs 750
.\scripts\watch-constraintos-poc.ps1 -Scenario perseverance -OpenRunFolder
pytest tests/test_end_to_end_fixture_poc_demo.py
```

This is a fixture-based, business-demo-friendly dry run. It shows scenario selection, contract/specification loading, candidate manifest/intake evidence, intake review, deterministic fixture byte loading, byte-loading review, fixture registry review, failure-matrix review, manual observation evidence, observation binding, evidence merge, fixture-only evaluation, final review packet, and demo summary. It writes run artifacts under `runs/poc-demo/<scenario>/<timestamp>/` and preserves no local image file opening, artifact download, network fetch, image decoding, CV/OCR provider integration, image generation/editing, source report mutation, or automatic approval.

### Current evidence-harness POC demo guide

Use this guide to explain the current evidence-harness demo separately from the later constraint-driven graphic output permutation target:

```powershell
pytest tests/test_current_evidence_harness_poc_demo_guide.py
```

Guide path:

```text
docs/800_Demos/Current_Evidence_Harness_POC_Demo_Guide.md
```

This guide is documentation-only. It explains that `scripts/watch-constraintos-poc.ps1` is the current evidence-harness demo and that the future output-permutation demo is intentionally banked for a later milestone.

### Candidate image byte loader demo watch script

Run a visible staged demo of the current candidate image byte-loading evidence path:

```powershell
.\scripts\watch-candidate-byte-loader.ps1
.\scripts\watch-candidate-byte-loader.ps1 -Record perseverance
.\scripts\watch-candidate-byte-loader.ps1 -Record supra_2jz_gte_twin_turbo -WatchDelayMs 750
pytest tests/test_candidate_image_byte_loader_demo_watch_script.py
```

This is a staged dry-run demonstration. It runs `cos-graphics-byte-loader minimal`, `review-packet`, `registry-review-packet`, and `failure-review-packet`; captures terminal transcript, watch output, JSON evidence files, and metadata under `runs/candidate-byte-loader/<record>/<timestamp>/`; and preserves no local file opening, artifact download, network fetch, image decoding, candidate scoring, source report mutation, or approval automation.

### Graphics contract watch script

```powershell
.\scripts\watch-graphics-contract.ps1
.\scripts\watch-graphics-contract.ps1 -Contract supra_2jz_gte_twin_turbo
.\scripts\watch-graphics-contract.ps1 -Contract perseverance -PlanOnly
.\scripts\watch-graphics-contract.ps1 -Contract hydroelectric_dam_powerhouse -WatchDelayMs 500
pytest tests/test_graphics_contract_watch_capture_script.py
```

This records the reusable graphics-contract runtime watch path and writes run artifacts under `runs/graphics-contracts/<contract>/<timestamp>/`.

## Perseverance graphics-validation fixture

```powershell
cos-graphics-validate perseverance --plan-only --format text
cos-graphics-validate perseverance --format text
cos-graphics-validate perseverance --format json
cos-graphics-validate perseverance --format json --output reports/perseverance-graphics-validation.json
pytest runtime/tests/test_graphics_perseverance_example.py
pytest tests/test_graphics_validation_cli.py
```

## Graphics contract commands

```powershell
pytest tests/test_graphics_contracts.py
cos-graphics-contracts list
cos-graphics-contracts show perseverance
cos-graphics-contracts show wind_turbine_nacelle
cos-graphics-contracts show hydroelectric_dam_powerhouse
cos-graphics-contracts show supra_2jz_gte_twin_turbo
cos-graphics-contracts --format json --output reports/graphics-contracts.json list
cos-graphics-contracts --format json show supra_2jz_gte_twin_turbo
pytest tests/test_graphics_contracts_cli.py
cos-graphics-contracts run perseverance --plan-only
cos-graphics-contracts run wind_turbine_nacelle
cos-graphics-contracts run hydroelectric_dam_powerhouse
cos-graphics-contracts run supra_2jz_gte_twin_turbo
cos-graphics-contracts --format json --output reports/supra-contract-runtime.json run supra_2jz_gte_twin_turbo
pytest tests/test_graphics_contract_runtime_bridge.py
cos-graphics-contracts run perseverance --plan-only --watch
cos-graphics-contracts run wind_turbine_nacelle --watch
cos-graphics-contracts run hydroelectric_dam_powerhouse --watch
cos-graphics-contracts run supra_2jz_gte_twin_turbo --watch
cos-graphics-contracts run supra_2jz_gte_twin_turbo --watch --watch-delay-ms 250
```

## Candidate evaluation and observation commands

```powershell
pytest tests/test_candidate_evaluation_adapter_design.py
pytest tests/test_candidate_manifest_schema.py
cos-graphics-candidates list
cos-graphics-candidates show perseverance
cos-graphics-candidates show supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/candidate-manifests.json list
pytest tests/test_candidate_manifest_discovery_cli.py
pytest tests/test_candidate_evaluation_report_contract.py
cos-graphics-candidates evaluate perseverance
cos-graphics-candidates evaluate supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-candidate-evaluation.json evaluate perseverance
pytest tests/test_fixture_only_candidate_evaluation.py
pytest tests/test_foundation_readiness_review.py
pytest tests/test_observation_adapter_design.py
cos-graphics-candidates observe perseverance
cos-graphics-candidates observe supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-observations.json observe perseverance
pytest tests/test_manual_observation_fixture_adapter.py
cos-graphics-candidates bind-observations perseverance
cos-graphics-candidates bind-observations supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-observation-binding.json bind-observations perseverance
pytest tests/test_observation_report_binding.py
cos-graphics-candidates merge-evidence perseverance
cos-graphics-candidates merge-evidence supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-merged-evidence.json merge-evidence perseverance
pytest tests/test_observation_evidence_merge.py
cos-graphics-candidates review-packet perseverance
cos-graphics-candidates review-packet supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-review-packet.json review-packet perseverance
pytest tests/test_candidate_review_packet.py
pytest tests/test_foundation_exit_review.py
```

## Candidate image byte loading design and contract verification

```powershell
pytest tests/test_real_candidate_image_intake_design.py
pytest tests/test_candidate_image_byte_loading_design.py
pytest tests/test_candidate_image_byte_loading_implementation_design.py
pytest tests/test_candidate_image_byte_loading_implementation_contract.py
pytest tests/test_candidate_image_byte_loading_pre_implementation_exit_review.py
pytest tests/test_candidate_image_byte_loading_minimal_implementation.py
```

These commands are design-only, contract-only, or helper-only. They do not open files, download artifacts, fetch network resources, decode images, inspect pixels, score candidates, mutate reports, choose providers, or approve candidates.

## Candidate image byte loading minimal CLI

```powershell
cos-graphics-byte-loader minimal perseverance
cos-graphics-byte-loader --format json minimal perseverance
cos-graphics-byte-loader --format json --output reports/perseverance-byte-loader.json minimal perseverance
cos-graphics-byte-loader minimal perseverance --fixture-artifact-uri artifact://external-candidates/perseverance/candidate-0001.png --fixture-artifact-hex 89504e470d0a1a0a
pytest tests/test_candidate_image_byte_loading_minimal_cli.py
```

This is a helper-only CLI. It uses the deterministic fixture artifact registry by default, or accepts fixture bytes through explicit `--fixture-artifact-uri` and `--fixture-artifact-hex` arguments. It does not open local files, download artifacts, fetch network resources, decode images, inspect pixels, score candidates, mutate reports, choose providers, or approve candidates.

## Candidate image byte loading minimal CLI review packet

```powershell
cos-graphics-byte-loader review-packet perseverance
cos-graphics-byte-loader --format json review-packet perseverance
cos-graphics-byte-loader --format json --output reports/perseverance-byte-loader-review-packet.json review-packet perseverance
cos-graphics-byte-loader review-packet perseverance --fixture-artifact-uri artifact://external-candidates/perseverance/candidate-0001.png --fixture-artifact-hex 89504e470d0a1a0a
pytest tests/test_candidate_image_byte_loading_minimal_cli_review_packet.py
pytest tests/test_candidate_image_byte_loading_minimal_cli_exit_review.py
```

## Candidate image byte loading fixture artifact registry

```powershell
cos-graphics-byte-loader minimal perseverance
cos-graphics-byte-loader review-packet perseverance
pytest tests/test_candidate_image_byte_loading_fixture_artifact_registry.py
```

The registry validates expected sha256, expected byte count, and declared media type before exposing deterministic fixture bytes to the in-memory artifact registry adapter.

## Candidate image byte loading fixture registry review packet

```powershell
cos-graphics-byte-loader registry-review-packet
cos-graphics-byte-loader --format json registry-review-packet
cos-graphics-byte-loader --format json --output reports/candidate-image-fixture-registry-review-packet.json registry-review-packet
pytest tests/test_candidate_image_byte_loading_fixture_registry_review_packet.py
pytest tests/test_candidate_image_byte_loading_fixture_registry_exit_review.py
```

This is a fixture-only review packet command. It reports registry identity, artifact descriptors, validation boundaries, and decision guardrails without exposing image bytes.

## Candidate image byte loading fixture registry failure matrix

```powershell
pytest tests/test_candidate_image_byte_loading_fixture_registry_failure_matrix.py
```

This is a fixture-only failure matrix. It covers invalid sha256, invalid byte count, invalid media type, invalid artifact URI, duplicate artifact ID, duplicate artifact URI, descriptor mutability violations, local file opening guardrail violations, network fetch guardrail violations, image decoding guardrail violations, and approval guardrail violations.

## Candidate image byte loading fixture registry failure review packet

```powershell
cos-graphics-byte-loader failure-review-packet
cos-graphics-byte-loader --format json failure-review-packet
cos-graphics-byte-loader --format json --output reports/candidate-image-fixture-registry-failure-review-packet.json failure-review-packet
pytest tests/test_candidate_image_byte_loading_fixture_registry_failure_review_packet.py
```

This is a fixture-only review packet command. It summarizes failure matrix identity, failure cases, fail-closed boundaries, and decision guardrails without executing failure mutations, exposing bytes, opening local files, downloading artifacts, fetching network resources, decoding images, scoring candidates, mutating reports, choosing providers, or approving candidates.

## Candidate image byte loading contract, discovery, and review packet

```powershell
pytest tests/test_candidate_image_byte_loading_contract.py
cos-graphics-candidates byte-loading-list
cos-graphics-candidates byte-loading-show perseverance
cos-graphics-candidates byte-loading-show supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/candidate-byte-loading-records.json byte-loading-list
pytest tests/test_candidate_image_byte_loading_discovery_cli.py
cos-graphics-candidates byte-loading-review-packet perseverance
cos-graphics-candidates byte-loading-review-packet supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-byte-loading-review-packet.json byte-loading-review-packet perseverance
pytest tests/test_candidate_image_byte_loading_review_packet.py
pytest tests/test_byte_loading_foundation_exit_review.py
```

## Candidate intake manifest commands

```powershell
pytest tests/test_candidate_intake_manifest_contract.py
cos-graphics-candidates intake-list
cos-graphics-candidates intake-show perseverance
cos-graphics-candidates intake-show supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/candidate-intake-manifests.json intake-list
pytest tests/test_candidate_intake_manifest_discovery_cli.py
cos-graphics-candidates intake-review-packet perseverance
cos-graphics-candidates intake-review-packet supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-intake-review-packet.json intake-review-packet perseverance
pytest tests/test_candidate_intake_review_packet.py
pytest tests/test_intake_foundation_exit_review.py
```

## Full recent graphics-validation verification set

```powershell
pytest runtime/tests/test_graphics_perseverance_example.py
pytest tests/test_graphics_validation_cli.py
pytest tests/test_graphics_contracts.py
pytest tests/test_graphics_contracts_cli.py
pytest tests/test_graphics_contract_runtime_bridge.py
pytest tests/test_graphics_contract_watch_capture_script.py
pytest tests/test_candidate_image_byte_loader_demo_watch_script.py
pytest tests/test_end_to_end_fixture_poc_demo.py
pytest tests/test_current_evidence_harness_poc_demo_guide.py
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
pytest tests/test_candidate_image_byte_loading_implementation_design.py
pytest tests/test_candidate_image_byte_loading_implementation_contract.py
pytest tests/test_candidate_image_byte_loading_pre_implementation_exit_review.py
pytest tests/test_candidate_image_byte_loading_minimal_implementation.py
pytest tests/test_candidate_image_byte_loading_minimal_cli.py
pytest tests/test_candidate_image_byte_loading_minimal_cli_review_packet.py
pytest tests/test_candidate_image_byte_loading_minimal_cli_exit_review.py
pytest tests/test_candidate_image_byte_loading_fixture_artifact_registry.py
pytest tests/test_candidate_image_byte_loading_fixture_registry_review_packet.py
pytest tests/test_candidate_image_byte_loading_fixture_registry_exit_review.py
pytest tests/test_candidate_image_byte_loading_fixture_registry_failure_matrix.py
pytest tests/test_candidate_image_byte_loading_fixture_registry_failure_review_packet.py
pytest tests/test_candidate_image_byte_loading_contract.py
pytest tests/test_candidate_image_byte_loading_discovery_cli.py
pytest tests/test_candidate_image_byte_loading_review_packet.py
pytest tests/test_byte_loading_foundation_exit_review.py
pytest tests/test_candidate_intake_manifest_contract.py
pytest tests/test_candidate_intake_manifest_discovery_cli.py
pytest tests/test_candidate_intake_review_packet.py
pytest tests/test_intake_foundation_exit_review.py
```

## Current contract keys

```text
perseverance
wind_turbine_nacelle
hydroelectric_dam_powerhouse
supra_2jz_gte_twin_turbo
```

## Current candidate manifest keys

Use these keys with `cos-graphics-candidates show`, `cos-graphics-candidates evaluate`, `cos-graphics-candidates observe`, `cos-graphics-candidates bind-observations`, `cos-graphics-candidates merge-evidence`, `cos-graphics-candidates review-packet`, `cos-graphics-candidates intake-show`, `cos-graphics-candidates intake-review-packet`, `cos-graphics-candidates byte-loading-show`, `cos-graphics-candidates byte-loading-review-packet`, and `cos-graphics-byte-loader`:

```text
perseverance
supra_2jz_gte
supra_2jz_gte_twin_turbo
```

## Guardrails

```text
- These commands are dry-run / fixture-only / design-only / contract-only / read-only / helper-only for graphics validation.
- These commands do not generate images.
- These commands do not evaluate real generated candidates yet.
- The end-to-end fixture POC demo, current evidence-harness POC demo guide, candidate byte-loader demo watch script, candidate image byte-loading minimal implementation, minimal CLI, minimal CLI review packet, fixture artifact registry, fixture registry review packet, fixture registry failure matrix, and fixture registry failure review packet are limited to explicit in-memory artifact registry / deterministic fixture bytes and descriptor-only/failure-matrix review.
- Real candidate image intake design, candidate image byte-loading design, implementation design/contract, pre-implementation exit review, byte-loading contract/discovery/review-packet fixtures, intake manifests, and intake review packets do not decode images.
- Approval expectations remain contract-driven and default uncertainty to needs_review.
```
