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

## LF4 example

The LF4 Engineering Atlas constraint pack captures the standing LF4 production standards:

- The image must be recognizably Cadillac ATS-V LF4-specific.
- It must not degrade into a generic GM V6.
- Twin-turbo routing and subsystem relationships must be mechanically plausible.
- Off-engine continuations must be shown schematically when necessary.

## Design note

Constraint Packs are not automatically merged into render specifications yet. This step establishes the validated, reusable pack format first. A later compiler step will apply packs to render specifications deterministically.
