# Constraint-Driven Graphic Output Permutation POC Contract

## Status

```text
demo: Constraint-Driven Graphic Output Permutation POC
status: contract-defined
track: Business Demo Visibility Track
milestone: docs/500_Milestones/Constraint_Driven_Graphic_Output_Permutation_POC_v1.md
phase: Phase 1 - contract and data model
scenario_key: supra_2jz_gte_twin_turbo
primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic
implementation_authority: fixture-safe-output-specifications-only
```

## Purpose

Define the deterministic, fixture-safe contract for the next product-shaped demo.

This contract describes what the output-permutation POC may write before any script or runtime implementation is added.

The POC target remains:

```text
input constraints + scenario instructions -> graphic output permutations -> validation evidence -> reviewable result
```

## Core rule

```text
The POC may define output specifications.
The POC may define controlled placeholder artifacts.
The POC may validate those specifications against loaded constraints.
The POC must not generate production artwork.
The POC must not inspect or decode real images.
The POC must not approve candidates automatically.
```

## Allowed artifact set

```text
graphic-output-manifest.json
graphic-output-permutations.json
graphic-output-validation.json
graphic-output-review-packet.json
index.html
run-metadata.json
```

## Artifact roles

### graphic-output-manifest.json

```text
role: run-level inventory
purpose: list each fixture-safe output permutation and explain why it exists
business_view: what variants were created and why
technical_view: stable permutation identifiers, scenario, constraint references, and traceability links
```

Required top-level fields:

```text
demo
scenario_key
use_case_title
run_id
created_at_local
final_decision
approval_allowed
permutation_count
permutation_ids
constraints_source
artifacts
```

### graphic-output-permutations.json

```text
role: controlled output specification set
purpose: define each fixture-safe output variant without generating a real image
business_view: what each output would emphasize
technical_view: deterministic specification data that later validation can inspect
```

Required top-level fields:

```text
demo
scenario_key
permutations
```

Required permutation fields:

```text
permutation_id
variant_name
business_intent
visual_strategy
required_constraints
emphasized_constraints
known_risks
explicit_non_goals
placeholder_artifact
expected_review_state
```

### graphic-output-validation.json

```text
role: deterministic validation evidence
purpose: record how each permutation maps to constraints
business_view: what was satisfied, missed, or uncertain
technical_view: traceable evidence rows per permutation and constraint
```

Required top-level fields:

```text
demo
scenario_key
validation_mode
final_decision
approval_allowed
permutation_results
```

Required permutation result fields:

```text
permutation_id
satisfied_constraints
missing_constraints
uncertain_constraints
blocked_claims
review_decision
approval_allowed
```

### graphic-output-review-packet.json

```text
role: reviewer-facing summary
purpose: make output permutations understandable to non-technical reviewers
business_view: which variant is most promising and why approval remains blocked
technical_view: summary of validation decisions and guardrails
```

Required top-level fields:

```text
demo
scenario_key
viewer_summary
recommended_reviewer_path
final_decision
approval_allowed
why_approval_is_blocked
next_recommended_action
```

### index.html

```text
role: browser-facing walkthrough
purpose: show constraints -> permutations -> validation -> needs_review
business_view: visual and narrative explanation of controlled output variants
technical_view: static rendering of the fixture-safe JSON contract data
```

### run-metadata.json

```text
role: traceability metadata
purpose: record where files were written and which scenario produced them
business_view: repeatable demo run identity
technical_view: deterministic run folder and guardrail summary
```

## Toyota Supra required baseline constraints

Every fixture-safe output permutation for the first scenario must reference these baseline constraints:

```text
- Toyota Supra Mk IV / A80 identity
- 2JZ-GTE inline-six identity
- sequential twin-turbo system
- not generic engine
- not V6
- not V8
- not rotary
- not RB26
- not LF4
- not B58
- technical graphic / publishing context
- uncertainty defaults to needs_review
- approval_allowed remains false
```

## Initial permutation IDs

```text
turbo_system_focus
inline_six_engine_identity_focus
technical_label_density_focus
reviewer_safe_minimal_focus
```

## Decision semantics

```text
pass:
- A fixture-safe output specification satisfies the explicitly listed constraints it claims to satisfy.

needs_review:
- A fixture-safe output specification leaves a constraint uncertain.
- A fixture-safe output specification intentionally avoids a visual claim that cannot be validated yet.
- The current implementation remains static, placeholder-based, or incomplete.

fail:
- A fixture-safe output specification contradicts a required constraint.
- A fixture-safe output specification claims a wrong engine family, layout, platform, or system.
- A fixture-safe output specification implies production artwork was generated.
```

## Approval rule

```text
approval_allowed: false
```

The POC may compare permutations, but approval must remain blocked until a later separately authorized milestone defines stronger evidence.

## Explicitly forbidden fields

The fixture-safe contract must not introduce fields that imply real image loading, image generation, or production artwork authority.

Forbidden field names:

```text
local_file_path
file_uri
source_image_path
generated_image_path
production_artwork_path
pixel_data
ocr_text
cv_provider
auto_approved
```

## Guardrails

```text
- No unrestricted image generation.
- No production artwork generation.
- No real local image input.
- No local_file_path loading.
- No file_uri loading.
- No artifact download.
- No network fetch.
- No image decoding.
- No pixel inspection.
- No CV/OCR provider integration.
- No automatic approval.
```

## Phase 1 done criteria

```text
[x] Contract document exists.
[x] Allowed artifact set is defined.
[x] Manifest shape is defined.
[x] Permutation shape is defined.
[x] Validation evidence shape is defined.
[x] Review packet shape is defined.
[x] Toyota Supra baseline constraints are defined.
[x] Initial permutation IDs are defined.
[x] Decision semantics are defined.
[x] Forbidden fields are documented.
[x] Guardrails are preserved.
[ ] Verification test result recorded.
```

## Verification command

```powershell
pytest tests/test_constraint_driven_graphic_output_permutation_contract.py
```
