# Candidate Evaluation Fixtures

This directory contains design-only and schema-only fixtures for future candidate graphics evaluation.

## Current fixtures

```text
candidate_evaluation_adapter.design.json
candidate_manifest.schema.json
perseverance_candidate_manifest.fixture.json
supra_2jz_gte_candidate_manifest.fixture.json
```

## Status

```text
adapter_status: design_only
manifest_status: static_fixture_only
implementation_status: not_started
image_generation_allowed: false
image_editing_allowed: false
real_candidate_image_ingestion_allowed: false
computer_vision_integration_allowed: false
initial_decision: needs_review
uncertainty_default: needs_review
```

## Purpose

The adapter design fixture defines the boundary between reusable graphics-validation contracts and future externally produced candidate graphics.

The candidate manifest schema defines the static manifest shape required before any future candidate-evaluation command can exist.

## Candidate manifest fixtures

The manifest fixtures bind externally produced candidate references to existing graphics-validation contract keys.

```text
perseverance_candidate_manifest.fixture.json:
  contract_key: perseverance

supra_2jz_gte_candidate_manifest.fixture.json:
  contract_key: supra_2jz_gte_twin_turbo
```

The fixture references are placeholders only. They do not load, decode, inspect, or evaluate image bytes.

## Verification

```powershell
pytest tests/test_candidate_evaluation_adapter_design.py
pytest tests/test_candidate_manifest_schema.py
```

## Guardrail

Candidate graphics are external inputs. ConstraintOS does not generate, edit, load, inspect, or approve images in these milestones.
