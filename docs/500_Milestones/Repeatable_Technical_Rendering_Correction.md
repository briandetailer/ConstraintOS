# Repeatable Technical Rendering Correction

## Status

```text
milestone: Repeatable Technical Rendering Correction
status: active
started_on: 2026-07-17
trigger: Workbench real-image output review failed
branch: phase-1-cli-tooling
```

## Incident

The packaged ConstraintOS Workbench successfully reached the image provider and produced PNG artifacts, but the resulting images failed the product requirement for repeatable technical drawings.

Observed failures included:

```text
- incorrect or invented engine geometry
- inconsistent component placement between candidates
- unreadable and hallucinated labels
- incorrect Toyota Supra / 2JZ-GTE identity text
- arbitrary turbo, intake, exhaust, and intercooler routing
- no stable camera, orientation, topology, or component registry
- no automatic rejection despite obvious technical invalidity
```

All reviewed outputs are rejected. They are not acceptable technical-drawing candidates.

## Root cause

The Workbench real-image path currently performs unconstrained text-to-image generation after the deterministic exercise pipeline. It does not use a canonical engine asset, locked camera, component geometry, reference-conditioned generation, deterministic label overlay, or technical validation gate.

The current path therefore proves provider connectivity only. It does not prove ConstraintOS-controlled technical illustration.

## Product correction

```text
text_to_image_role: exploratory_reference_only
text_to_image_production_technical_output: prohibited
canonical_geometry_required: true
locked_camera_required: true
locked_render_preset_required: true
component_registry_required: true
provider_generated_labels: prohibited
technical_labels: deterministic_overlay_only
production_output_without_canonical_asset: fail_closed
```

A generated raster may be retained as an exploratory reference artifact, but it must never be represented as a repeatable technical drawing or a production candidate.

## Correct production architecture

### 1. Canonical source geometry

A verified Toyota 2JZ-GTE source asset must be imported and normalized. The source may be a controlled Blender scene or a supported 3D interchange asset converted into one.

The canonical asset record must include:

```text
- asset identifier and version
- source/provenance record
- file digest
- unit scale
- coordinate system
- object/component inventory
- engine orientation definition
- approved visible and hidden components
```

### 2. Deterministic renderer

The technical base plate must be rendered from the canonical asset using locked values for:

```text
- camera transform and projection
- object visibility
- line-render settings
- lighting
- materials or monochrome treatment
- resolution and crop
- background
- render engine and version
```

The same asset, render preset, and view definition must produce the same composition on repeated runs within an explicitly defined pixel-difference tolerance.

### 3. Deterministic annotation layer

The image provider must not render titles, labels, legends, measurements, arrows, or callout text.

All annotation must be generated separately as SVG or another deterministic vector layer using:

```text
- approved label strings
- component identifiers
- stored anchor points
- controlled typography
- controlled leader-line routing
- collision and margin checks
```

### 4. Validation gates

A technical output must fail closed unless all required gates pass:

```text
- canonical_asset_present
- canonical_asset_digest_matches
- expected_component_inventory_present
- locked_view_definition_present
- render_preset_version_matches
- output_dimensions_match
- forbidden_raster_text_absent
- annotation_strings_registry_backed
- callout_targets_registry_backed
- orientation_matches_view_contract
- repeat_render_difference_within_tolerance
```

Manual review remains required after automated validation, but manual review must not substitute for missing deterministic foundations.

## Workbench behavior correction

The Workbench must separate two distinct capabilities:

```text
Explore with Generated Raster References
- optional OpenAI image generation
- stochastic
- may contain invented geometry
- no technical approval path
- stored under exploratory-reference artifacts

Render Repeatable Technical Drawing
- canonical geometry required
- deterministic renderer required
- deterministic annotation overlay required
- blocked until all preflight gates are satisfied
```

The existing label `Run with Real Images` is misleading and must be replaced. The UI must not describe provider-generated rasters as technical drawing candidates.

## Implementation slices

```text
[ ] Add executable technical-rendering policy manifest
[ ] Add tests enforcing text-to-image exploratory-only status
[ ] Rename Workbench real-image path and artifact manifest
[ ] Remove label-generation instructions from image-provider prompts
[ ] Add canonical-asset preflight status to Workbench
[ ] Add fail-closed Repeatable Technical Drawing action
[ ] Define canonical 2JZ-GTE asset manifest and object registry
[ ] Add locked Blender render preset and view contract
[ ] Add deterministic SVG annotation pipeline
[ ] Add repeat-render comparison gate
[ ] Package the deterministic renderer with the Workbench
[ ] Re-run the Supra use case and record acceptance evidence
```

## Acceptance criteria

This milestone is complete only when:

```text
1. Repeated runs from the same canonical asset and view produce the same technical base plate within the approved tolerance.
2. No generated text appears inside the raster base plate.
3. Every visible annotation comes from an approved registry entry.
4. Every leader line resolves to a registered component anchor.
5. The output is recognizably and verifiably a Toyota 2JZ-GTE inline-six twin-turbo engine.
6. A missing or changed canonical asset blocks production rendering.
7. Text-to-image output cannot enter the production approval path.
```

## Guardrails

```text
[x] Reject the four reviewed PNG outputs
[x] Do not solve the failure by adding more prompt prose alone
[x] Do not ask an image model to generate technical labels
[x] Do not claim repeatability from stochastic text-to-image output
[x] Preserve provider generation only as an explicitly exploratory feature
[x] Require canonical geometry for production technical drawings
```
