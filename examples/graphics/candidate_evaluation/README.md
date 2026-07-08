# Candidate Evaluation Fixtures

This directory contains design-only, schema-only, read-only discovery, and fixture-only report contract artifacts for future candidate graphics evaluation.

## Current fixtures

```text
candidate_evaluation_adapter.design.json
candidate_manifest.schema.json
candidate_evaluation_report.schema.json
perseverance_candidate_manifest.fixture.json
supra_2jz_gte_candidate_manifest.fixture.json
perseverance_candidate_evaluation_report.fixture.json
supra_2jz_gte_candidate_evaluation_report.fixture.json
```

## Status

```text
adapter_status: design_only
manifest_status: static_fixture_only
discovery_status: read_only
report_contract_status: fixture_only
implementation_status: not_started
image_generation_allowed: false
image_editing_allowed: false
real_candidate_image_ingestion_allowed: false
computer_vision_integration_allowed: false
candidate_evaluation_ran: false
initial_decision: needs_review
uncertainty_default: needs_review
```

## Purpose

The adapter design fixture defines the boundary between reusable graphics-validation contracts and future externally produced candidate graphics.

The candidate manifest schema defines the static manifest shape required before any future candidate-evaluation command can exist.

The candidate manifest discovery CLI lists and shows static manifest summaries without evaluating candidate images.

The candidate evaluation report contract defines the future report shape before any candidate evaluation behavior is implemented.

## Candidate manifest fixtures

The manifest fixtures bind externally produced candidate references to existing graphics-validation contract keys.

```text
perseverance_candidate_manifest.fixture.json:
  manifest_key: perseverance
  contract_key: perseverance

supra_2jz_gte_candidate_manifest.fixture.json:
  manifest_key: supra_2jz_gte
  contract_key: supra_2jz_gte_twin_turbo
```

The fixture references are placeholders only. They do not load, decode, inspect, or evaluate image bytes.

## Candidate evaluation report fixtures

The report fixtures bind to the static candidate manifests and describe the future evidence/report shape.

```text
perseverance_candidate_evaluation_report.fixture.json:
  candidate_manifest_key: perseverance
  contract_key: perseverance
  recommended_decision: needs_review
  evidence_status: not_observed

supra_2jz_gte_candidate_evaluation_report.fixture.json:
  candidate_manifest_key: supra_2jz_gte
  contract_key: supra_2jz_gte_twin_turbo
  recommended_decision: needs_review
  evidence_status: not_observed
```

The report fixtures do not claim that candidate evaluation has run. They exist to lock the report contract before implementation.

## Read-only discovery commands

```powershell
cos-graphics-candidates list
cos-graphics-candidates show perseverance
cos-graphics-candidates show supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/candidate-manifests.json list
```

## Verification

```powershell
pytest tests/test_candidate_evaluation_adapter_design.py
pytest tests/test_candidate_manifest_schema.py
pytest tests/test_candidate_manifest_discovery_cli.py
pytest tests/test_candidate_evaluation_report_contract.py
```

## Guardrail

Candidate graphics are external inputs. ConstraintOS does not generate, edit, load, inspect, evaluate, or approve images in these milestones.
