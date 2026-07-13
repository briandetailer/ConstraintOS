# Fixture-Safe Visual Placeholder Evidence Summary Cards

## Status

```text
demo: Fixture-Safe Visual Placeholder Refinement
status: evidence-summary-cards-defined
phase: Phase 3 - evidence summary cards
phase_status: ready-for-verification
track: Business Demo Visibility Track
milestone: docs/500_Milestones/Fixture_Safe_Visual_Placeholder_Refinement_v1.md
contract: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Refinement_Contract.md
panel_design: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Panel_Design.md
scenario_key: supra_2jz_gte_twin_turbo
primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic
implementation_authority: fixture-safe-visual-placeholders-only
assistant_ran_tests: false
assistant_ran_demo: false
```

## Purpose

Define the evidence summary cards that appear beside or inside each fixture-safe placeholder panel.

The goal is to make each placeholder easier to review without expanding authority beyond deterministic fixture evidence.

```text
placeholder panel -> evidence summary card -> needs_review explanation -> approval_allowed false
```

## Evidence summary rule

```text
Evidence summary cards may summarize fixture evidence, but they must not score artwork, inspect pixels, or approve output.
```

Every evidence summary card must show:

```text
- permutation_id
- satisfied fixture constraints
- visible uncertainty
- blocked claims
- reviewer note
- review_decision: needs_review
- approval_allowed: false
```

## Shared card layout

```text
evidence_summary_card:
- card title
- constraint coverage chips
- visible uncertainty note
- blocked claim list
- reviewer interpretation note
- review state footer
```

## Required evidence card set

```text
1. turbo_system_focus
   evidence_card_title: Turbo System Evidence
   satisfied_constraints: Toyota Supra A80, 2JZ-GTE, sequential twin-turbo
   visible_uncertainty: schematic layout is placeholder-only
   blocked_claims: final artwork, physical accuracy approval, image-derived verification
   review_decision: needs_review
   approval_allowed: false

2. inline_six_engine_identity_focus
   evidence_card_title: Inline-Six Identity Evidence
   satisfied_constraints: Toyota Supra A80, 2JZ-GTE inline-six, wrong-engine exclusions
   visible_uncertainty: identity emphasis is placeholder-only
   blocked_claims: final artwork, hidden mechanical correctness approval, image-derived verification
   review_decision: needs_review
   approval_allowed: false

3. technical_label_density_focus
   evidence_card_title: Label Density Evidence
   satisfied_constraints: technical graphic context, label comparison, fixture-defined tokens
   visible_uncertainty: label density requires reviewer judgment
   blocked_claims: final label placement, production-ready diagram approval, image-derived verification
   review_decision: needs_review
   approval_allowed: false

4. reviewer_safe_minimal_focus
   evidence_card_title: Reviewer-Safe Evidence
   satisfied_constraints: validated claims only, visible uncertainty, approval blocked
   visible_uncertainty: withheld details remain unverified
   blocked_claims: final artwork, automatic approval, unstated mechanical claims
   review_decision: needs_review
   approval_allowed: false
```

## Allowed evidence tokens

```text
- evidence_summary_card
- constraint_coverage_chip
- visible_uncertainty_note
- blocked_claim_item
- reviewer_interpretation_note
- review_state_footer
```

## Blocked evidence tokens

```text
- numeric_quality_score
- visual_similarity_score
- pixel_confidence
- ocr_confidence
- cv_detection_confidence
- approval_score
- pass_fail_artwork_grade
- generated_asset_reference
```

## Reviewer copy requirements

Each evidence summary card must include reviewer-facing copy that says:

```text
- This card summarizes fixture evidence only.
- This card does not inspect or grade final artwork.
- Uncertainty remains needs_review.
- approval_allowed remains false.
```

## Traceability requirements

Each card must map summary evidence back to at least one loaded constraint category:

```text
engine_identity -> 2JZ-GTE inline-six identity
vehicle_identity -> Toyota Supra A80 / Mk IV identity
turbo_identity -> sequential twin-turbo identity
wrong_engine_exclusion -> not V6 / not V8 / not rotary / not RB26 / not LF4 / not B58
review_safety -> uncertainty defaults to needs_review and approval_allowed remains false
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

## Phase 3 done criteria

```text
[x] Evidence summary card document exists.
[x] Shared card layout is defined.
[x] Four required evidence cards are defined.
[x] Allowed evidence tokens are listed.
[x] Blocked evidence tokens are listed.
[x] Reviewer copy requirements preserve fixture-safe scope.
[x] Traceability requirements are defined.
[x] Guardrails are preserved.
[ ] Verification test result recorded.
```

## Verification command

```powershell
pytest tests/test_fixture_safe_visual_placeholder_evidence_summary_cards.py
```