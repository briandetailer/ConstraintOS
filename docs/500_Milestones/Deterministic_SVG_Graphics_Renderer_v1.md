# Deterministic SVG Graphics Renderer v1

## Status

```text
milestone: Deterministic SVG Graphics Renderer v1
status: active
started_on: 2026-07-13
track: Business Demo Visibility Track
previous_milestone: docs/500_Milestones/Fixture_Safe_Placeholder_Browser_Implementation_v1.md
script: scripts/watch-constraintos-output-poc.ps1
scenario_key: supra_2jz_gte_twin_turbo
primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic
implementation_authority: deterministic-svg-output-only
assistant_ran_tests: false
assistant_ran_demo: false
```

## Purpose

Move from browser-only placeholder panels to real deterministic SVG graphic artifacts that are generated from the existing fixture-safe output permutations.

```text
output permutations -> deterministic SVG graphics -> browser display -> structural evidence -> needs_review
```

## Product promise for this milestone

```text
- Write one SVG file for each Toyota Supra output permutation.
- Store SVG files under runs/output-poc/<scenario>/<timestamp>/graphics/.
- Link generated SVG files from index.html.
- Record generated SVG artifact paths in run-metadata.json.
- Preserve needs_review for every variant.
- Preserve approval_allowed: false.
- Keep SVG output deterministic, fixture-defined, and non-image-derived.
```

## Target SVG artifacts

```text
graphics/turbo_system_focus.svg
graphics/inline_six_engine_identity_focus.svg
graphics/technical_label_density_focus.svg
graphics/reviewer_safe_minimal_focus.svg
```

## Renderer boundary

```text
allowed:
- SVG markup generated from deterministic fixture data
- rectangles
- lines
- text labels
- callout groups
- traceability labels
- review footer text

blocked:
- generated raster artwork
- external image references
- local image input
- image decoding
- pixel inspection
- CV/OCR provider integration
- automatic approval
```

## Structural validation target

```text
- each SVG file is listed in metadata
- each SVG file is linked from index.html
- each SVG preserves permutation_id
- each SVG preserves review_decision: needs_review
- each SVG preserves approval_allowed: false
- no SVG claims final artwork or production approval
```

## Implementation changes under verification

```text
script_update: scripts/watch-constraintos-output-poc.ps1
command_reference_update: docs/700_Use_Cases/Graphics_Validation_Command_Reference.md
verification: pytest tests/test_constraint_driven_graphic_output_permutation_watch_script.py
status: ready-for-implementation
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

## Done criteria

```text
[x] Milestone exists.
[x] Previous browser implementation milestone is referenced.
[x] Deterministic SVG output target is defined.
[x] Required SVG artifact paths are listed.
[x] Renderer boundary is defined.
[x] Structural validation target is defined.
[x] Blocked scope is preserved.
[ ] SVG output implemented.
[ ] Verification result recorded.
```

## Verification command

```powershell
pytest tests/test_deterministic_svg_graphics_renderer_milestone.py
pytest tests/test_constraint_driven_graphic_output_permutation_watch_script.py
```
