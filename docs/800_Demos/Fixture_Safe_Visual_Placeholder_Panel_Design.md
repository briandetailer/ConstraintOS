# Fixture-Safe Visual Placeholder Panel Design

## Status

```text
demo: Fixture-Safe Visual Placeholder Refinement
status: panel-design-defined
phase: Phase 2 - browser placeholder panel design
phase_status: ready-for-verification
track: Business Demo Visibility Track
milestone: docs/500_Milestones/Fixture_Safe_Visual_Placeholder_Refinement_v1.md
contract: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Refinement_Contract.md
scenario_key: supra_2jz_gte_twin_turbo
primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic
implementation_authority: fixture-safe-visual-placeholders-only
assistant_ran_tests: false
assistant_ran_demo: false
```

## Purpose

Define the browser-visible placeholder panel design for the four Toyota Supra output permutations before any browser implementation changes are made.

The design goal is reviewer clarity:

```text
same constraints -> visibly different fixture-safe placeholder panels -> same needs_review decision
```

## Panel design rule

```text
Panels may improve visual comparison, but they must remain deterministic, fixture-defined, non-image-derived, and blocked from approval.
```

Every panel must show:

```text
- permutation_id
- business intent
- fixture-safe visual placeholder type
- deterministic panel components
- constraint trace summary
- evidence summary
- uncertainty note
- review_decision: needs_review
- approval_allowed: false
```

## Shared browser layout

```text
panel_shell:
- permutation title
- one-line business intent
- deterministic schematic or text-first placeholder area
- constraint trace chips
- evidence summary card
- uncertainty banner
- review state footer
```

## Required panel set

```text
1. turbo_system_focus
   visual_placeholder_type: schematic_block_panel
   panel_components:
   - title band: Turbo System Focus
   - schematic blocks: engine core, twin turbo A, twin turbo B, charge path, exhaust path
   - constraint chips: 2JZ-GTE, sequential twin-turbo, Toyota Supra A80
   - uncertainty banner: schematic placeholder only, not final artwork
   - review footer: needs_review / approval_allowed false

2. inline_six_engine_identity_focus
   visual_placeholder_type: text_first_panel
   panel_components:
   - title band: Inline-Six Identity Focus
   - identity blocks: inline-six, 2JZ-GTE, Mk IV Supra
   - exclusion chips: not V6, not V8, not rotary, not RB26, not LF4, not B58
   - uncertainty banner: identity placeholder only, not final artwork
   - review footer: needs_review / approval_allowed false

3. technical_label_density_focus
   visual_placeholder_type: label_density_panel
   panel_components:
   - title band: Technical Label Density Focus
   - label zones: core labels, turbo labels, flow labels, warning labels
   - density indicator: high label density for review comparison
   - uncertainty banner: label layout placeholder only, not final artwork
   - review footer: needs_review / approval_allowed false

4. reviewer_safe_minimal_focus
   visual_placeholder_type: reviewer_safe_minimal_panel
   panel_components:
   - title band: Reviewer-Safe Minimal Focus
   - validated claim blocks: Toyota Supra A80, 2JZ-GTE, sequential twin-turbo
   - hidden/withheld claim note: uncertain details remain out of visual emphasis
   - uncertainty banner: conservative placeholder only, not final artwork
   - review footer: needs_review / approval_allowed false
```

## Allowed deterministic visual tokens

```text
- panel_shell
- title_band
- schematic_block
- identity_block
- exclusion_chip
- constraint_chip
- evidence_chip
- density_indicator
- uncertainty_banner
- review_footer
```

## Blocked visual tokens

```text
- raster_image
- generated_artwork
- source_image
- decoded_pixels
- ocr_overlay
- cv_detection_box
- external_asset
- downloaded_asset
- approval_badge
```

## Browser copy requirements

Each panel must include reviewer-facing copy that says:

```text
- This is a deterministic placeholder, not final artwork.
- This panel is derived from fixture constraints, not image inspection.
- Uncertainty remains needs_review.
- approval_allowed remains false.
```

## Traceability requirements

Each panel must map at least one visual token back to at least one constraint category:

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

## Phase 2 done criteria

```text
[x] Panel design document exists.
[x] Shared browser layout is defined.
[x] Four required placeholder panels are defined.
[x] Allowed deterministic visual tokens are listed.
[x] Blocked visual tokens are listed.
[x] Browser copy requirements preserve fixture-safe scope.
[x] Traceability requirements are defined.
[x] Guardrails are preserved.
[ ] Verification test result recorded.
```

## Verification command

```powershell
pytest tests/test_fixture_safe_visual_placeholder_panel_design.py
```