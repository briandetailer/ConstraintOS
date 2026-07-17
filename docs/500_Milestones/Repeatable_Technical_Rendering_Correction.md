# Repeatable Technical Rendering Correction

## Status

```text
milestone: Repeatable Technical Rendering Correction
status: active
started_on: 2026-07-17
trigger: Workbench real-image output review failed
branch: phase-1-cli-tooling
current_checkpoint: Toyota source-plate path accepted; responsive v3 presentation pending local verification
next_major_scenario: NASA Perseverance registered geometry rendering
```

## Original example-selection requirement

The NASA, Toyota, and other demonstration scenarios were selected because useful example information is available on the web. The correction must preserve that requirement.

```text
example_selection: sufficient web-available reference information
proprietary_3d_purchase_required: false
source_preference: official and authoritative web sources first
production_capability: limited to what the available source package can support
```

ConstraintOS must turn those sources into versioned, hashed, auditable reference packages. It must not ignore the available references and ask an image model to recreate the subject from text alone.

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

The Workbench real-image path performed unconstrained text-to-image generation after the deterministic exercise pipeline. It did not condition generation on the registered official web sources, use a canonical source plate or geometry asset, apply a locked view, or enforce a technical validation gate.

That path proved provider connectivity only. It did not prove ConstraintOS-controlled technical illustration.

## Corrected source architecture

A canonical source asset may be two-dimensional or three-dimensional. The source type determines what ConstraintOS is allowed to produce.

### Mode A: geometry render

Use when official or verified 3D geometry is available.

```text
accepted_sources:
- official_web_3d_geometry
- verified_local_geometry

allowed:
- locked deterministic camera views
- deterministic line and material rendering
- repeat-render comparison
- deterministic SVG annotation overlays

required:
- downloaded source file
- provenance record
- file digest
- normalized geometry
- component inventory
- locked camera and render preset
```

The NASA Perseverance example qualifies for this path because official NASA/JPL geometry is available online in downloadable 3D formats.

### Mode B: source-plate annotation

Use when an authoritative fixed-view image is available but verified 3D geometry is not.

```text
accepted_sources:
- official_web_2d_source_plate

allowed:
- repeatable output from the registered fixed source plate
- deterministic crop and scaling
- deterministic SVG titles, labels, callouts, and legends
- component anchors registered against the fixed plate

blocked:
- invented camera angles
- exploded views not present in source evidence
- hidden geometry reconstruction
- claims of 3D geometric repeatability
```

The Toyota 2JZ-GTE example qualifies for this path. Toyota provides an official fixed-view engine image and an official Supra technical release. Those sources support repeatable annotated plates from the registered view, not arbitrary generated engine views.

### Mode C: reference bundle only

Use when documentation is sufficient for validation and terminology but not for a production base plate.

```text
allowed:
- identity validation
- terminology registry evidence
- component and constraint research

blocked:
- production technical base plate
```

## Product correction

```text
text_to_image_role: exploratory_reference_only
text_to_image_production_technical_output: prohibited
canonical_source_package_required: true
canonical_asset_may_be_2d_or_3d: true
capability_must_not_exceed_source_package: true
provider_generated_labels: prohibited
technical_labels: deterministic_overlay_only
production_output_without_required_source_evidence: fail_closed
```

A generated raster may be retained as an exploratory artifact, but it must never be represented as a repeatable technical drawing or a production candidate.

## Source-package ingestion

Registered web sources are materialized locally rather than committed as untracked binaries.

The preparation workflow must:

```text
1. read config/technical-reference-source-registry.json
2. download only registered ingestion sources
3. preserve the source page and download URL
4. calculate SHA-256 for every downloaded file
5. write source-package-manifest.json
6. record usage-terms review status
7. remain production_ready: false until later technical preflight gates pass
```

Materialized files are stored under `reference-sources/`, which is excluded from source control.

## Validation gates

A technical output must fail closed unless the gates applicable to its production mode pass:

```text
- canonical_source_package_present
- source_provenance_recorded
- source_usage_terms_recorded
- canonical_asset_present
- canonical_asset_digest_matches
- requested_capability_supported_by_source_class
- expected_component_inventory_present
- locked_view_or_source_plate_definition_present
- render_preset_version_matches
- output_dimensions_match
- forbidden_raster_text_absent
- annotation_strings_registry_backed
- callout_targets_registry_backed
- callout_layout_bounds_passed
- orientation_matches_view_contract
- repeat_render_difference_within_tolerance
```

Manual review remains required after automated validation, but manual review must not substitute for missing deterministic foundations.

## Workbench behavior correction

The Workbench separates three distinct capabilities:

```text
Explore Generated Raster References
- optional OpenAI image generation
- stochastic
- may contain invented geometry
- no technical approval path

Render Registered Toyota Source Plate
- authoritative fixed source plate required
- deterministic crop and registry-backed annotation
- novel views and hidden geometry blocked

Render from Registered Geometry
- verified 3D geometry required
- deterministic camera and renderer
- deterministic annotation overlay
```

Provider-generated rasters are not described as technical drawing candidates.

## Toyota acceptance evidence

The Toyota source package and technical release were materialized successfully on Windows. The source-policy test group reported `15 passed`, and both the NASA and Toyota preparation scripts reported `source_files_materialized`.

The packaged Toyota Workbench path was then exercised twice. Both runs completed in `source_plate_render` mode. The user confirmed the expected repeat-render responses were correct and supplied a screenshot of the actual source-backed plate.

The screenshot established:

```text
[x] official Toyota source plate visibly used
[x] deterministic title and registry-backed callout overlay present
[x] engine identity recognizably Toyota 2JZ-GTE
[x] no image-model-generated technical text
[x] repeat-render workflow completed
[x] manual-review and approval blocking retained
```

The screenshot also revealed two presentation defects:

```text
- source-backed SVG displayed in a scrolling iframe rather than scaling to the Workbench card
- right-side labels extended beyond the visible presentation area
```

The v3 presentation contract corrects those defects by embedding the SVG as a responsive image, moving right-side labels inside the output bounds, and adding a fail-closed callout-layout bounds gate. Because the contract, render preset, and component registry version changed, the v3 renderer intentionally starts a new repeatability baseline.

## Implementation slices

```text
[x] Add executable technical-rendering policy manifest
[x] Add tests enforcing text-to-image exploratory-only status
[x] Add web-available reference-source strategy to policy
[x] Register official NASA and Toyota source packages
[x] Add local source materialization and SHA-256 manifest workflow
[x] Exclude materialized source binaries from source control
[x] Rename Workbench real-image path and artifact manifest
[x] Remove label-generation instructions from image-provider prompts
[x] Add source-package preflight status to Workbench
[x] Add fail-closed source-plate rendering action
[x] Ingest and hash official Toyota source plate and technical release
[x] Define Toyota fixed-view contract and component anchors
[x] Add deterministic SVG annotation pipeline for Toyota plate
[x] Add repeat-render comparison gate for Toyota source plates
[x] Package the deterministic Toyota source-backed renderer with Workbench
[x] Run Toyota use case and record initial acceptance evidence
[x] Add responsive plate presentation and callout-layout bounds gate
[x] Ingest and hash official NASA Perseverance geometry
[ ] Define NASA component registry, camera, and render preset
[ ] Add deterministic NASA geometry renderer
[ ] Add NASA repeat-render comparison gate
[ ] Package the NASA geometry renderer with Workbench
[ ] Run NASA use case and record acceptance evidence
```

## Acceptance criteria

This milestone is complete only when:

```text
1. The registered web source files are materialized and hash-verified.
2. Output capability cannot exceed the registered source class.
3. Repeated runs from the same source package produce the same base plate within the approved tolerance.
4. No generated text appears inside the raster base plate.
5. Every visible annotation comes from an approved registry entry.
6. Every leader line resolves to a registered component anchor.
7. Every callout label and route remains inside the output safe area.
8. Toyota output is recognizably and verifiably based on the official 2JZ-GTE source plate.
9. NASA output is recognizably and verifiably rendered from the official Perseverance geometry.
10. Missing or changed source assets block production rendering.
11. Text-to-image output cannot enter the production approval path.
```

## Guardrails

```text
[x] Reject the four reviewed PNG outputs
[x] Preserve the original web-available-example requirement
[x] Do not require a proprietary 3D purchase for every scenario
[x] Do not solve the failure by adding more prompt prose alone
[x] Do not ask an image model to generate technical labels
[x] Do not claim repeatability from stochastic text-to-image output
[x] Preserve provider generation only as an explicitly exploratory feature
[x] Require a canonical source package for production technical drawings
[x] Limit each scenario to capabilities supported by its source evidence
[x] Fail closed when registered callout presentation is out of bounds
```
