# Candidate Evaluation Adapter Design Fixtures

This directory contains design-only fixtures for future candidate graphics evaluation.

## Current fixture

```text
candidate_evaluation_adapter.design.json
```

## Status

```text
status: design_only
implementation_status: not_started
image_generation_allowed: false
real_candidate_image_ingestion_allowed: false
computer_vision_integration_allowed: false
uncertainty_default: needs_review
```

## Purpose

The fixture defines the boundary between reusable graphics-validation contracts and future externally produced candidate graphics.

It does not implement candidate evaluation yet.

## Guardrail

Candidate graphics are external inputs. ConstraintOS does not generate images in this design milestone.
