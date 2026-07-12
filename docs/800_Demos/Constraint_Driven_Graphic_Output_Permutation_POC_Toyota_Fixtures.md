# Constraint-Driven Graphic Output Permutation POC Toyota Fixtures

## Status

```text
demo: Constraint-Driven Graphic Output Permutation POC
status: fixture-data-defined
track: Business Demo Visibility Track
milestone: docs/500_Milestones/Constraint_Driven_Graphic_Output_Permutation_POC_v1.md
contract: docs/800_Demos/Constraint_Driven_Graphic_Output_Permutation_POC_Contract.md
phase: Phase 2 - deterministic Toyota fixture data
scenario_key: supra_2jz_gte_twin_turbo
primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic
implementation_authority: deterministic-fixture-data-only
```

## Purpose

Define the deterministic Toyota Supra fixture data that will later feed the output-permutation POC script.

This document is data-contract work only. It defines controlled output specifications and review expectations. It does not generate images, decode images, inspect pixels, fetch network resources, or approve candidates.

## Fixture data rule

```text
Each fixture permutation must be deterministic.
Each fixture permutation must reference the Toyota Supra A80 / 2JZ-GTE constraint set.
Each fixture permutation must explain its business intent.
Each fixture permutation must declare known risks and non-goals.
Each fixture permutation must end in expected_review_state: needs_review.
Each fixture permutation must use a placeholder_artifact identifier, not a file path.
```

## Shared baseline constraints

```text
Toyota Supra Mk IV / A80 identity
2JZ-GTE inline-six identity
sequential twin-turbo system
not generic engine
not V6
not V8
not rotary
not RB26
not LF4
not B58
technical graphic / publishing context
uncertainty defaults to needs_review
approval_allowed remains false
```

## Fixture permutation records

### 1. turbo_system_focus

```text
permutation_id: turbo_system_focus
variant_name: Sequential twin-turbo system focus
business_intent: Show why the technical graphic must communicate a sequential twin-turbo 2JZ-GTE system rather than a generic forced-induction engine.
visual_strategy: Emphasize the turbo-system callout layer, airflow path intent, and twin-turbo distinction while keeping engine identity constraints visible.
required_constraints:
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
emphasized_constraints:
- sequential twin-turbo system
- 2JZ-GTE inline-six identity
known_risks:
- turbo routing may be over-implied before real artwork evidence exists
- visual simplification may hide sequential system nuance
explicit_non_goals:
- do not claim production artwork was generated
- do not claim pixel-level validation
- do not claim exact factory routing verification
placeholder_artifact: fixture-placeholder://output-poc/supra/turbo-system-focus
expected_review_state: needs_review
```

### 2. inline_six_engine_identity_focus

```text
permutation_id: inline_six_engine_identity_focus
variant_name: 2JZ-GTE inline-six identity focus
business_intent: Show why the output must remain a Toyota Supra A80 / 2JZ-GTE inline-six and must not drift into a V6, V8, rotary, RB26, LF4, or B58 representation.
visual_strategy: Emphasize engine-family identity, inline-six layout, and wrong-engine exclusion constraints before turbo-system detail.
required_constraints:
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
emphasized_constraints:
- Toyota Supra Mk IV / A80 identity
- 2JZ-GTE inline-six identity
- not V6
- not V8
- not rotary
- not RB26
- not LF4
- not B58
known_risks:
- identity focus may under-explain the sequential twin-turbo system
- viewers may expect actual engine artwork in this phase
explicit_non_goals:
- do not claim production artwork was generated
- do not use real local image input
- do not represent this as image generation
placeholder_artifact: fixture-placeholder://output-poc/supra/inline-six-identity-focus
expected_review_state: needs_review
```

### 3. technical_label_density_focus

```text
permutation_id: technical_label_density_focus
variant_name: Technical label-density focus
business_intent: Show how the same constraints can produce a denser technical publishing variant for reviewers who need more explanation.
visual_strategy: Increase specification density, callout density, and constraint traceability while retaining the same Toyota Supra / 2JZ-GTE baseline.
required_constraints:
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
emphasized_constraints:
- technical graphic / publishing context
- uncertainty defaults to needs_review
known_risks:
- too much label density may reduce business readability
- dense specification may look more authoritative than evidence supports
explicit_non_goals:
- do not claim automatic approval
- do not claim CV/OCR inspection
- do not claim production artwork was generated
placeholder_artifact: fixture-placeholder://output-poc/supra/technical-label-density-focus
expected_review_state: needs_review
```

### 4. reviewer_safe_minimal_focus

```text
permutation_id: reviewer_safe_minimal_focus
variant_name: Reviewer-safe minimal focus
business_intent: Show a conservative output specification that exposes only validated requirements and clearly parks uncertain claims in needs_review.
visual_strategy: Keep the variant minimal, highlight only the safest baseline constraints, and make approval blocking visible.
required_constraints:
- Toyota Supra Mk IV / A80 identity
- 2JZ-GTE inline-six identity
- sequential twin-turbo system
- not generic engine
- uncertainty defaults to needs_review
- approval_allowed remains false
emphasized_constraints:
- uncertainty defaults to needs_review
- approval_allowed remains false
known_risks:
- conservative output may feel less impressive to business reviewers
- minimal display may not satisfy viewers asking for concrete generated output
explicit_non_goals:
- do not claim production artwork was generated
- do not imply final approval
- do not imply all technical details are verified
placeholder_artifact: fixture-placeholder://output-poc/supra/reviewer-safe-minimal-focus
expected_review_state: needs_review
```

## Expected manifest summary

```text
permutation_count: 4
permutation_ids:
- turbo_system_focus
- inline_six_engine_identity_focus
- technical_label_density_focus
- reviewer_safe_minimal_focus
final_decision: needs_review
approval_allowed: false
```

## Expected validation summary

```text
turbo_system_focus:
  review_decision: needs_review
  approval_allowed: false
  primary_uncertainty: sequential system detail remains fixture-safe and not image-verified

inline_six_engine_identity_focus:
  review_decision: needs_review
  approval_allowed: false
  primary_uncertainty: identity strategy is specified, not visually generated or inspected

technical_label_density_focus:
  review_decision: needs_review
  approval_allowed: false
  primary_uncertainty: label density may imply more evidence than the fixture currently has

reviewer_safe_minimal_focus:
  review_decision: needs_review
  approval_allowed: false
  primary_uncertainty: intentionally conservative output does not prove full generated-output capability
```

## Forbidden data in fixture records

Fixture records must not contain image-loading, image-generation, or production-artwork authority fields.

```text
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
- Fixture data only.
- No generated final graphics.
- No production artwork generation.
- No real local image input.
- No artifact download.
- No network fetch.
- No image decoding.
- No pixel inspection.
- No CV/OCR provider integration.
- No automatic approval.
```

## Phase 2 done criteria

```text
[x] Toyota fixture data document exists.
[x] Four permutation records are defined.
[x] Each permutation includes business intent.
[x] Each permutation includes visual strategy.
[x] Each permutation references Toyota Supra / 2JZ-GTE constraints.
[x] Each permutation includes known risks.
[x] Each permutation includes explicit non-goals.
[x] Each permutation uses a placeholder artifact identifier.
[x] Each permutation defaults to needs_review.
[x] approval_allowed remains false.
[x] Guardrails are preserved.
[ ] Verification test result recorded.
```

## Verification command

```powershell
pytest tests/test_constraint_driven_graphic_output_permutation_toyota_fixtures.py
```
