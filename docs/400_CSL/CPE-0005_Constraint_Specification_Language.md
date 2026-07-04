# CPE-0005 Constraint Specification Language

Status: Draft
Version: 0.1

## Purpose
The Constraint Specification Language (CSL) is the structured language used to describe artifacts, constraints, evidence, rendering intent, validation rules, and approval criteria.

CSL is not a prompt. CSL is a machine-readable specification format that can be compiled into renderer-specific instructions and validator-specific tests.

## Design Goals

- Human-readable
- Machine-parseable
- Renderer-independent
- Validator-aware
- Versionable
- Traceable
- Extensible across domains

## Core Object Model

```yaml
artifact:
  id: PLATE-0001
  type: technical_plate
  title: Example artifact
  domain: automotive
  status: draft

subject:
  type: engine
  family: LF4
  evidence:
    - EV-0001

view:
  camera:
    orientation: front_left
    azimuth_degrees: 30
    elevation_degrees: 15

constraints:
  - id: C-0001
    statement: Artifact must depict a V6 engine.
    severity: blocker
    validation_method: visual_semantic
    acceptance: visible architecture is consistent with six-cylinder V layout

renderer:
  target: any
  style_profile: technical_atlas

validation:
  required_pass:
    blocker: 100
    major: 95
```

## Constraint Types

- semantic
- geometric
- topological
- visual
- stylistic
- publishing
- evidence
- negative
- workflow

## Severity Levels

- blocker: artifact cannot be approved
- major: artifact normally requires revision
- minor: artifact may be approved with notes
- advisory: informational or preference-level issue

## Validation Outcomes

- pass
- fail
- uncertain
- not_applicable
- blocked_by_missing_evidence

## Compiler Semantics
A compiler converts CSL into renderer-specific instructions. The compiler must not silently discard constraints. Unsupported constraints must be reported.

## Validator Semantics
A validator evaluates an artifact against CSL constraints. Validators must represent uncertainty explicitly and must not convert uncertainty into pass without human approval.

## Minimal CSL Record
A valid CSL artifact must include:

- artifact id
- artifact type
- subject
- at least one constraint
- renderer target or profile
- validation threshold

## Future Work
The CSL will require a formal JSON Schema, grammar reference, examples, and compatibility versioning.
