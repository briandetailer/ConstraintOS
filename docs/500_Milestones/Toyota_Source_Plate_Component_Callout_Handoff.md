# Toyota Source Plate Component Callout Handoff

## Status

```text
milestone_slice: Toyota Source Plate Registry-Backed Component Callouts
status: implemented_pending_local_verification
implemented_on: 2026-07-17
branch: phase-1-cli-tooling
source_mode: official_web_2d_source_plate
approval_allowed: false
```

## Accepted prior evidence

Two consecutive source-backed v1 runs completed successfully in the packaged Workbench:

```text
20260717-011811
20260717-012021
```

Because the v1 renderer failed closed on repeat-output mismatch, successful completion of the second run establishes that the original source-backed composition was byte-repeatable.

No screenshot is required as repeatability evidence. The technical render manifest and matching SHA-256 values are the authoritative evidence.

## Slice purpose

Advance the Toyota example from a deterministic identity plate to a deterministic annotated plate without inventing geometry or asking an image provider to generate labels.

## Registered visible callouts

```text
2JZ-COMP-001  Intake manifold plenum
2JZ-COMP-002  Engine oil filler cap
2JZ-COMP-003  Cylinder-head cover
2JZ-COMP-004  ETCS throttle-control actuator
```

These callouts are limited to clearly visible targets on the registered official Toyota source image.

## Deliberately blocked callouts

```text
- individual turbocharger location
- hidden exhaust routing
- hidden intake routing
- internal engine geometry
- exploded-view relationships
- inferred rear-side components
```

The plate may state the documented two-way twin-turbo system identity, but it must not point to turbocharger hardware that is not clearly exposed in the fixed source view.

## Implementation

```text
component_registry:
  config/technical-component-registries/toyota-supra-a80-2jz-gte-source-plate-v1.json

source_plate_contract:
  config/technical-source-plate-contracts/toyota-supra-a80-2jz-gte-v1.json
  contract_version: 2.0.0
  render_preset_version: source-plate-svg/v2

workbench_entry:
  apps/constraintos_workbench/app_v3.py
```

The v2 renderer:

```text
- verifies the materialized source package and SHA-256
- reads every label and anchor from the component registry
- places annotation text outside the source raster
- draws deterministic leader lines and anchor circles
- records the component registry identity and callout count
- records annotation_strings_registry_backed: true
- records callout_targets_registry_backed: true
- records hidden_geometry_inferred: false
- compares output only against prior runs with the same contract and render preset
- fails closed on repeat-render mismatch
```

## Local verification

```powershell
cd D:\Code\ConstraintOS

git pull --rebase origin phase-1-cli-tooling

pytest `
  tests/test_constraintos_workbench_app.py `
  tests/test_technical_rendering_policy.py `
  tests/test_technical_reference_source_registry.py `
  tests/test_prepare_technical_reference_source_package.py

.\scripts\package-constraintos-workbench-app.ps1 -Clean

& "D:\Code\ConstraintOS\dist\ConstraintOS Workbench\ConstraintOS Workbench.exe"
```

Run `Render Registered Toyota Source Plate` twice.

Expected first v2 result:

```text
Repeat-render comparison: baseline_created
Registered callouts: 4
```

Expected second v2 result:

```text
Repeat-render comparison: passed
Registered callouts: 4
Current output SHA-256 == Previous output SHA-256
```

## Visual review target

For visual QA, review the actual plate—not the App status text.

Use either:

```text
Source-Backed Toyota Technical Plate panel
Open source-backed plate link
```

The visual review checks callout placement, line routing, readability, and whether every anchor lands on the intended visible component.

## Guardrails

```text
[x] No provider-generated labels
[x] No invented engine geometry
[x] No hidden turbocharger callout
[x] No novel camera angle
[x] No unregistered annotation text
[x] No unregistered callout target
[x] No approval path
[x] Manual visual review still required
```
