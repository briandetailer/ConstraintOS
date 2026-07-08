# Candidate Evaluation Fixtures

This directory contains design-only, schema-only, read-only discovery, fixture-only report contract, and fixture-only evaluation artifacts for future candidate graphics evaluation.

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
fixture_only_evaluation_status: available
implementation_status: foundation_only
image_generation_allowed: false
image_editing_allowed: false
real_candidate_image_ingestion_allowed: false
computer_vision_integration_allowed: false
candidate_evaluation_source: static_report_fixture
initial_decision: needs_review
uncertainty_default: needs_review
approval_allowed: false
```

## Purpose

The adapter design fixture defines the boundary between reusable graphics-validation contracts and future externally produced candidate graphics.

The candidate manifest schema defines the static manifest shape required before any future candidate-evaluation command can exist.

The candidate manifest discovery CLI lists and shows static manifest summaries without evaluating candidate images.

The candidate evaluation report contract defines the future report shape before any real candidate evaluation behavior is implemented.

The fixture-only candidate evaluation command loads a static manifest fixture and its matching static report fixture, validates their binding, and reports the fixture recommendation.

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

The report fixtures bind to the static candidate manifests and describe the fixture-only evidence/report shape.

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

The report fixtures do not claim that real candidate evaluation has run. They exist to lock the report contract before real image ingestion.

## Read-only discovery commands

```powershell
cos-graphics-candidates list
cos-graphics-candidates show perseverance
cos-graphics-candidates show supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/candidate-manifests.json list
```

## Fixture-only evaluation commands

```powershell
cos-graphics-candidates evaluate perseverance
cos-graphics-candidates evaluate supra_2jz_gte_twin_turbo
cos-graphics-candidates --format json --output reports/perseverance-candidate-evaluation.json evaluate perseverance
```

These commands load static manifest and report fixtures only. They do not load, decode, inspect, or evaluate image bytes.

## Verification

```powershell
pytest tests/test_candidate_evaluation_adapter_design.py
pytest tests/test_candidate_manifest_schema.py
pytest tests/test_candidate_manifest_discovery_cli.py
pytest tests/test_candidate_evaluation_report_contract.py
pytest tests/test_fixture_only_candidate_evaluation.py
```

## Guardrail

Candidate graphics are external inputs. ConstraintOS does not generate, edit, load, inspect, or approve images in these milestones. Fixture-only candidate evaluation reports `needs_review` from static report fixtures only.
