# Fixture-Safe Visual Placeholder Refinement Contract

## Status

```text
demo: Fixture-Safe Visual Placeholder Refinement
status: contract-defined
phase: Phase 1 - placeholder refinement contract
phase_status: ready-for-verification
track: Business Demo Visibility Track
milestone: docs/500_Milestones/Fixture_Safe_Visual_Placeholder_Refinement_v1.md
previous_output_permutation_poc: docs/500_Milestones/Constraint_Driven_Graphic_Output_Permutation_POC_v1.md
previous_feedback_loop: docs/800_Demos/Constraint_Driven_Graphic_Output_Permutation_POC_Feedback_Loop.md
scenario_key: supra_2jz_gte_twin_turbo
primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic
implementation_authority: fixture-safe-visual-placeholders-only
assistant_ran_tests: false
assistant_ran_demo: false
```

## Purpose

Define the allowed contract for fixture-safe visual placeholder refinement before any browser or runtime changes are made.

This contract keeps the work inside deterministic product-demo scope:

```text
constraints -> fixture-safe placeholder visuals -> evidence summary -> needs_review
```

## Core rule

```text
Fixture-safe placeholders may make output specifications easier to compare, but they must not become generated artwork, inspected images, or approval automation.
```

A placeholder is allowed only when it is:

```text
- deterministic
- fixture-defined
- non-image-derived
- reviewer-visible
- traceable to loaded constraints
- explicitly marked needs_review
- blocked from approval
```

## Placeholder record schema

Each placeholder record must use this shape:

```text
placeholder_id:
permutation_id:
scenario_key:
business_intent:
visual_placeholder_type:
fixture_components:
constraint_trace:
evidence_summary:
uncertainty_notes:
review_decision: needs_review
approval_allowed: false
```

## Allowed visual_placeholder_type values

```text
schematic_block_panel
text_first_panel
label_density_panel
constraint_trace_panel
evidence_summary_card
reviewer_safe_minimal_panel
```

## Allowed fixture_components

```text
- deterministic rectangles, bands, and containers
- deterministic labels and captions
- deterministic callout placeholders
- deterministic component tokens
- deterministic traceability rows
- deterministic risk and uncertainty notes
- deterministic evidence chips
```

## Blocked placeholder fields

The placeholder schema must not include these fields:

```text
image_path
local_file_path
file_uri
source_image_uri
source_image_bytes
pixel_data
ocr_text
cv_provider_result
generated_image_uri
approval_result
```

## Toyota Supra placeholder requirements

Every Toyota Supra placeholder must preserve these constraints:

```text
- Toyota Supra A80 / Mk IV identity
- 2JZ-GTE inline-six identity
- sequential twin-turbo identity
- not V6
- not V8
- not rotary
- not RB26
- not LF4
- not B58
- technical graphic context
- uncertainty defaults to needs_review
- approval_allowed remains false
```

## Required placeholder set

```text
1. turbo_system_focus
   visual_placeholder_type: schematic_block_panel
   required emphasis: sequential twin-turbo identity
   review_decision: needs_review
   approval_allowed: false

2. inline_six_engine_identity_focus
   visual_placeholder_type: text_first_panel
   required emphasis: 2JZ-GTE inline-six identity and wrong-engine exclusions
   review_decision: needs_review
   approval_allowed: false

3. technical_label_density_focus
   visual_placeholder_type: label_density_panel
   required emphasis: denser technical callout comparison
   review_decision: needs_review
   approval_allowed: false

4. reviewer_safe_minimal_focus
   visual_placeholder_type: reviewer_safe_minimal_panel
   required emphasis: only validated claims and visible uncertainty
   review_decision: needs_review
   approval_allowed: false
```

## Review semantics

```text
needs_review:
- Default decision for every fixture-safe placeholder.
- Used when a placeholder is useful for business review but is not final artwork.

approval_allowed: false
- Required for every placeholder.
- Cannot be changed by placeholder refinement.
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

## Phase 1 done criteria

```text
[x] Contract document exists.
[x] Placeholder record schema is defined.
[x] Allowed placeholder types are defined.
[x] Allowed fixture components are defined.
[x] Blocked placeholder fields are listed.
[x] Toyota Supra placeholder requirements are defined.
[x] Required placeholder set is defined.
[x] Review semantics preserve needs_review.
[x] approval_allowed remains false.
[x] Blocked scope is preserved.
[ ] Verification test result recorded.
```

## Verification command

```powershell
pytest tests/test_fixture_safe_visual_placeholder_refinement_contract.py
```
