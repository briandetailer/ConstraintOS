# Candidate Evaluation Adapter Design

## Purpose

This document defines the design boundary for evaluating externally produced candidate graphics against reusable ConstraintOS graphics-validation contracts.

The adapter is intentionally design-only at this stage. It does not generate images, edit images, ingest real image bytes, call computer-vision services, or approve generated graphics automatically.

## Problem being solved

ConstraintOS needs a safe boundary between:

```text
- reusable graphics-validation contracts
- externally produced candidate images
- evidence collection
- constraint evaluation
- approval recommendation
```

The adapter must prevent a plausible-looking graphic from being approved unless the available evidence supports the required subject identity, geometry, label, placement, and style constraints.

## Design status

```text
status: design_only
implementation: not_started
image_generation: not_allowed
candidate_image_processing: not_implemented
approval_automation_change: not_allowed
uncertainty_default: needs_review
```

## Adapter role

The candidate evaluation adapter is responsible for translating an external candidate reference plus a graphics contract into a normalized evaluation request.

It is not responsible for generating the candidate image.

It is not responsible for overriding the contract approval policy.

It is not responsible for approving uncertain results.

## Inputs

The adapter accepts a candidate manifest, not raw uncontrolled image generation instructions.

Required candidate manifest fields:

```text
candidate_id
contract_key
candidate_reference
candidate_source
submitted_at
```

Recommended candidate manifest fields:

```text
source_prompt_id
source_prompt_text
negative_prompt_text
producer
model_or_tool
render_settings
image_sha256
media_type
width
height
notes
```

The `candidate_reference` can later point to a local path, repository artifact, object-store URI, or connector file reference. In this design milestone, it remains a reference only.

## Contract inputs

The adapter consumes an existing graphics-validation contract.

Required contract fields:

```text
contract.id
contract.mode
subject.name
subject.identity_constraints
subject.forbidden_substitutions
rendering_requirements
required_labels
constraint_groups
decision_policy
approval_contract
```

## Adapter stages

```text
1. ingest_candidate_manifest
2. validate_candidate_manifest
3. resolve_graphics_contract
4. map_contract_constraints
5. request_observation_evidence
6. normalize_observation_evidence
7. score_constraints
8. build_evidence_report
9. recommend_approval_decision
```

The `request_observation_evidence` stage is a future integration point. It may eventually call image inspection, human review, or deterministic metadata checks. It is not implemented in this milestone.

## Evidence model

The adapter should produce evidence records that are explicit and traceable.

Each evidence item should include:

```text
constraint_id
constraint_group
claim
observed_status
evidence_source
confidence
notes
```

Allowed `observed_status` values:

```text
satisfied
missing
ambiguous
contradicted
not_observed
```

## Decision model

Allowed approval decisions remain contract-driven:

```text
approved
needs_review
rejected
```

Decision rules:

```text
- approved requires all required constraints to be satisfied with sufficient evidence.
- needs_review is required when evidence is missing, ambiguous, incomplete, or uncertain.
- rejected is allowed when evidence contradicts required subject identity, geometry, labels, placement, or forbidden-substitution constraints.
```

The uncertainty default is always:

```text
needs_review
```

## Hard guardrails

```text
- The adapter must not generate images.
- The adapter must not edit images.
- The adapter must not silently approve missing evidence.
- The adapter must not treat aesthetic quality as a substitute for technical correctness.
- The adapter must not approve candidate graphics when required evidence is ambiguous.
- The adapter must preserve contract allowed decisions.
- The adapter must preserve contract uncertainty behavior.
```

## Candidate reference boundary

Candidate graphics are external inputs.

The adapter may later accept references such as:

```text
local_path
artifact_uri
connector_file_reference
object_store_uri
```

But this design does not implement loading, decoding, rendering, OCR, or vision inspection.

## Non-goals

```text
- No image generation pipeline.
- No candidate image upload workflow.
- No generated image storage policy.
- No computer vision provider choice.
- No human review UI.
- No final approval automation.
```

## Future implementation path

A future milestone may add a candidate evaluation manifest schema and fixture-only CLI path such as:

```text
cos-graphics-candidate evaluate <candidate-manifest>
```

That command is not available in this milestone.

Before any such command is implemented, the command reference must be updated in the same implementation slice.
