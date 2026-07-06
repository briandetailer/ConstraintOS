# Constraint Packs

Constraint Packs are reusable groups of requirements, negative constraints, and validation gates.

They exist so common standards do not have to be copied manually into every render specification.

## Purpose

```text
Constraint Pack
  ↓
Render Specification
  ↓
Validation Pipeline
```

A render specification describes one artifact candidate. A constraint pack describes reusable standards that can be applied to many artifact candidates.

## Current schema

A constraint pack contains:

- `constraint_pack`: pack identity, status, and version.
- `requirements`: positive requirements that must be satisfied.
- `negative_constraints`: things the artifact must not do.
- `validation.gates`: gates used by the validation pipeline.

## Render specification references

When a pack is applied, the resulting render specification records the pack under `constraint_packs`.

```yaml
constraint_packs:
  - id: CPACK-0001
    version: "0.1"
    title: LF4 Engineering Atlas Constraint Pack
```

Render specification schema validation now checks that these references use `CPACK-0000` style IDs.

## Applying a pack

`apply_constraint_pack` merges a pack into a render specification deterministically:

- Existing requirements, negative constraints, and validation gates are preserved.
- Pack entries are appended only when their IDs are not already present.
- A `constraint_packs` reference is added to the resulting render specification.
- The source render specification and constraint pack are not mutated.
- Duplicate IDs with identical content are skipped.
- Duplicate IDs with different content are rejected instead of silently overwritten.

## CLI usage

Apply a pack and write the merged render specification to a file:

```powershell
cos-apply-constraints examples/render/lf4_engine_render_specification.yaml examples/constraint_packs/lf4_engine_constraint_pack.yaml --output .constraintos/render/lf4-applied.yaml
```

Apply multiple packs in order:

```powershell
cos-apply-constraints examples/render/lf4_engine_render_specification.yaml examples/constraint_packs/lf4_engine_constraint_pack.yaml examples/constraint_packs/another_pack.yaml --output .constraintos/render/applied.yaml
```

Print JSON output instead of YAML:

```powershell
cos-apply-constraints examples/render/lf4_engine_render_specification.yaml examples/constraint_packs/lf4_engine_constraint_pack.yaml --format json
```

## LF4 example

The LF4 Engineering Atlas constraint pack captures the standing LF4 production standards:

- The image must be recognizably Cadillac ATS-V LF4-specific.
- It must not degrade into a generic GM V6.
- Twin-turbo routing and subsystem relationships must be mechanically plausible.
- Off-engine continuations must be shown schematically when necessary.

## Design note

Constraint Packs now have a validated schema, deterministic applicator, CLI entry point, validated render-specification reference format, and duplicate-ID conflict detection. Multiple packs can be applied in a stable order before runtime or validation consumes the resulting render specification.
