# Milestone: Constraint Pack Traceability

Constraint Pack traceability is the first end-to-end provenance milestone for render-contract workflows.

## Goal

When a reusable Constraint Pack is applied to a render specification, the resulting pack reference must remain visible through planning, validation, remediation, revision, and approval outputs.

This prevents the system from losing the standards context that produced a pass, failure, remediation action, revision request, or approval decision.

## Traceability path

```text
Constraint Pack
  ↓
Render Specification constraint_packs
  ↓
Render Contract Runtime artifact.constraint_packs
  ↓
Validation Report validation_report.constraint_packs
  ↓
Failure Report failure_report.constraint_packs
  ↓
Remediation Plan remediation_plan.constraint_packs
  ↓
Revision Request revision_request.constraint_packs
  ↓
Approval Decision approval.constraint_packs
```

## CLI coverage

Traceability is visible through these commands:

```powershell
cos-apply-constraints examples/render/lf4_engine_render_specification.yaml examples/constraint_packs/lf4_engine_constraint_pack.yaml --format json
```

```powershell
cos-runtime examples/render/lf4_engine_render_specification.yaml --render-contract --constraint-pack examples/constraint_packs/lf4_engine_constraint_pack.yaml --plan-only
```

```powershell
cos-validate examples/render/lf4_engine_render_specification.yaml --constraint-pack examples/constraint_packs/lf4_engine_constraint_pack.yaml --evidence examples/validation/lf4_passing_evidence.yaml
```

## Current guarantees

- Constraint Pack references are idempotent when the same pack is applied more than once.
- Existing render-specification entries win when IDs are already present.
- Malformed validation-time `constraint_packs` references are rejected.
- JSON outputs preserve pack references in all relevant headers.
- Text summaries report applied pack counts where useful.

## Out of scope

This milestone does not add image generation, image inspection, Blender automation, Illustrator export, or visual validation. It only guarantees that standards provenance is not lost as data moves through the current deterministic runtime and validation layers.
