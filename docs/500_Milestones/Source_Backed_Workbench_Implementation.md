# Source-Backed Workbench Implementation

## Status

```text
milestone_slice: Source-Backed Workbench Implementation
status: implementation-complete-local-verification-pending
implemented_on: 2026-07-17
branch: phase-1-cli-tooling
source_package_evidence: 15 passed; NASA and Toyota source_files_materialized
```

## Purpose

Replace the rejected unconstrained real-image Workbench path with three explicitly separated capabilities:

```text
1. Run Deterministic Demo
2. Explore Generated Raster References
3. Render Registered Toyota Source Plate
```

The image provider is now exploratory only. The Toyota technical path uses the materialized official web source package and deterministic SVG composition.

## Implemented behavior

### Exploratory provider path

```text
button: Explore Generated Raster References
artifact_directory: exploratory-generated-references
manifest: exploratory-reference-manifest.json
artifact_role: exploratory_reference_only
technical_output_allowed: false
production_approval_allowed: false
```

The provider prompt explicitly prohibits words, letters, numbers, labels, legends, measurements, arrows, callout lines, diagrams, approval marks, and title blocks.

### Toyota source-backed path

```text
button: Render Registered Toyota Source Plate
production_mode: source_plate_annotation
canonical_source: toyota-2jz-gte-official-image-1993
contract: constraintos-source-plate/toyota-supra-a80-2jz-gte/v1
render_preset: source-plate-svg/v1
output: deterministic SVG
approval_allowed: false
review_decision: needs_review
```

Preflight fails closed unless:

```text
- the registered source-plate contract exists
- the Toyota source-package manifest exists
- preflight_status is source_files_materialized
- the registered source record exists
- the source plate file exists
- the observed SHA-256 matches the source-package manifest
```

The output contains the unmodified registered Toyota raster as its base source and a deterministic metadata overlay generated from the source-plate contract. No provider-generated labels or geometry are used.

### Repeat-render gate

The first source-backed render records:

```text
repeat_render_comparison.status: baseline_created
```

A subsequent render from the same source digest and contract must produce the same SVG digest and record:

```text
repeat_render_comparison.status: passed
```

A changed output fails closed.

## Packaging behavior

The Workbench packager now:

```text
- packages apps/constraintos_workbench/app_v2.py
- copies scripts/
- copies config/
- copies reference-sources/toyota_supra_a80_2jz_gte when materialized
- warns and leaves source-backed rendering blocked when the source package is absent
```

The packaged README clearly distinguishes exploratory raster generation from registered source-backed rendering.

## Compatibility behavior

`apps/constraintos_workbench/app.py` is now a compatibility launcher that loads the source-backed application. Running the legacy source path can no longer open the rejected unconstrained Workbench UI.

## Implementation commits

```text
78f0baa feat: add source-backed Workbench application
278b135 feat: register Toyota source-plate render contract
52cbe0f feat: package source-backed Workbench and Toyota reference package
66ea0fc tests: cover source-backed Workbench rendering
33849cb refactor: route legacy Workbench entry to source-backed app
```

## Local acceptance procedure

```powershell
git pull --rebase origin phase-1-cli-tooling

pytest `
  tests/test_constraintos_workbench_app.py `
  tests/test_technical_rendering_policy.py `
  tests/test_technical_reference_source_registry.py `
  tests/test_prepare_technical_reference_source_package.py

.\scripts\package-constraintos-workbench-app.ps1 -Clean

& "D:\Code\ConstraintOS\dist\ConstraintOS Workbench\ConstraintOS Workbench.exe"
```

Expected browser state:

```text
Registered Toyota source package
Status: ready
Ready for local source-backed draft: true
Production ready: false
```

Run `Render Registered Toyota Source Plate` twice.

First run acceptance:

```text
technical-render-manifest.json
repeat_render_comparison.status: baseline_created
```

Second run acceptance:

```text
technical-render-manifest.json
repeat_render_comparison.status: passed
previous_output_sha256 == current_output_sha256
```

## Current capability boundary

This slice produces a repeatable fixed-view Toyota identity plate. It does not yet provide component callouts, new camera angles, exploded views, hidden geometry, or a NASA geometry render. Those remain separate follow-on slices.
