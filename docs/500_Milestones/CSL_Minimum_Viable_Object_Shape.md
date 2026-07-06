# CSL Minimum Viable Object Shape

## Purpose

This note defines the first concrete object shape for CSL so future schema, compiler, validator, and SDK work has a stable target.

CSL v1 should remain JSON/YAML-based. A custom DSL can compile down to this shape later, but the v1 contract should be easy for .NET, Node.js, JavaScript, C#, CI/CD tools, and external generators to produce and consume.

## Design goals

The minimum viable CSL shape must support:

- explicit CSL versioning
- stable spec identity
- named entity references
- dimensional constraints
- relational/geometric constraints
- recursive groups
- AND, OR, and unary NOT
- full-tree validation reporting
- deterministic validation outcomes
- portable JSON/YAML representation

## Top-level CSL document

```json
{
  "csl_version": "csl/v1",
  "id": "CSL-SPEC-0001",
  "name": "Example bracket validation spec",
  "description": "Validates critical dimensions and relationships for a generated bracket.",
  "entities": [],
  "constraints": [],
  "groups": [],
  "root_group_id": "GROUP-ROOT"
}
```

### Required fields

| Field | Required | Purpose |
| --- | --- | --- |
| `csl_version` | yes | Version of the CSL document contract. |
| `id` | yes | Stable identifier for the spec. |
| `name` | yes | Human-readable name. |
| `entities` | yes | Named geometric or logical things constraints can reference. |
| `constraints` | yes | Atomic constraints. |
| `groups` | yes | Logical composition of constraints and other groups. |
| `root_group_id` | yes | Entry point for validation. |
| `description` | no | Human-readable context. |

## Entity object

Entities identify the things a constraint can point at. They are intentionally generic at v1 so CAD, image, document, rendering, and workflow validators can all use the same reference concept.

```json
{
  "id": "ENTITY-HOLE-A",
  "type": "circle",
  "label": "left mounting hole",
  "selector": {
    "kind": "feature_id",
    "value": "hole_a"
  }
}
```

### Entity fields

| Field | Required | Purpose |
| --- | --- | --- |
| `id` | yes | Stable entity identifier used by constraints. |
| `type` | yes | Domain-level entity type, such as `edge`, `circle`, `datum`, `plane`, `region`, `artifact`, or `feature`. |
| `label` | no | Human-readable label. |
| `selector` | yes | How the validator locates the entity in the generated artifact. |
| `metadata` | no | Optional domain-specific context. |

## Constraint object

Constraints are atomic validation checks. Groups compose them into larger validation logic.

```json
{
  "id": "CONSTRAINT-WIDTH",
  "type": "dimensional",
  "entity_id": "ENTITY-BRACKET-BODY",
  "measurement": "width_mm",
  "operator": "between",
  "expected": {
    "min": 49.8,
    "max": 50.2,
    "unit": "mm"
  },
  "severity": "error"
}
```

### Constraint fields

| Field | Required | Purpose |
| --- | --- | --- |
| `id` | yes | Stable constraint identifier. |
| `type` | yes | Constraint category, such as `dimensional` or `geometric_relation`. |
| `severity` | yes | `error`, `warning`, or `info`. |
| `entity_id` | conditional | Primary entity reference for single-entity constraints. |
| `entity_ids` | conditional | Multi-entity references for relational constraints. |
| `measurement` | conditional | Measurement name for dimensional constraints. |
| `relation` | conditional | Relation name for geometric constraints. |
| `operator` | yes | Evaluation operator. |
| `expected` | yes | Expected value, bounds, tolerance, or relation payload. |
| `metadata` | no | Optional domain-specific context. |

## Constraint types

### Dimensional constraint

Dimensional constraints validate scalar measurements, bounds, and tolerances.

Example operators:

- `equals`
- `between`
- `less_than`
- `less_than_or_equal`
- `greater_than`
- `greater_than_or_equal`
- `within_tolerance`

### Geometric relation constraint

Geometric relation constraints validate relationships between named entities.

```json
{
  "id": "CONSTRAINT-HOLES-CONCENTRIC",
  "type": "geometric_relation",
  "entity_ids": ["ENTITY-HOLE-A", "ENTITY-HOLE-B"],
  "relation": "parallel",
  "operator": "within_tolerance",
  "expected": {
    "tolerance_degrees": 0.25
  },
  "severity": "error"
}
```

Initial relation names:

- `parallel`
- `perpendicular`
- `concentric`
- `collinear`
- `coplanar`
- `angle_between`
- `distance_between`
- `inside_region`
- `outside_region`

## Group object

Groups compose constraints and groups into validation trees.

```json
{
  "id": "GROUP-ROOT",
  "operator": "AND",
  "children": [
    {"type": "constraint", "id": "CONSTRAINT-WIDTH"},
    {"type": "group", "id": "GROUP-HOLE-PATTERN"}
  ]
}
```

### Group fields

| Field | Required | Purpose |
| --- | --- | --- |
| `id` | yes | Stable group identifier. |
| `operator` | yes | `AND`, `OR`, or `NOT`. |
| `children` | yes | Child references. |
| `description` | no | Human-readable explanation. |
| `metadata` | no | Optional domain-specific context. |

### Group rules

- `AND` may have one or more children.
- `OR` may have one or more children.
- `NOT` must have exactly one child.
- Children may reference either constraints or groups.
- Nesting is recursive.
- Mixed operators are allowed in different branches.

## Child reference object

```json
{"type": "constraint", "id": "CONSTRAINT-WIDTH"}
```

```json
{"type": "group", "id": "GROUP-HOLE-PATTERN"}
```

## Full-tree validation reporting

CSL validation should emit a full evaluation tree by default.

The result for every constraint and group should be recorded, even when a logical operator could have short-circuited. This is required for auditability and for explaining why a validation result was accepted or rejected.

## Minimum validation result shape

```json
{
  "csl_validation_result": {
    "spec_id": "CSL-SPEC-0001",
    "csl_version": "csl/v1",
    "status": "failed",
    "successful": false,
    "root_group_id": "GROUP-ROOT"
  },
  "tree": {},
  "issues": []
}
```

### Constraint evaluation record

```json
{
  "id": "CONSTRAINT-WIDTH",
  "record_type": "constraint",
  "constraint_type": "dimensional",
  "status": "passed",
  "expected": {"min": 49.8, "max": 50.2, "unit": "mm"},
  "actual": {"value": 50.0, "unit": "mm"},
  "issues": []
}
```

### Group evaluation record

```json
{
  "id": "GROUP-ROOT",
  "record_type": "group",
  "operator": "AND",
  "status": "failed",
  "children": [],
  "issues": []
}
```

### NOT reporting rule

When `NOT` wraps a constraint or group, the report must preserve both:

- the inner pre-inversion result
- the outer inverted NOT result

This keeps audit logs readable. Example: the inner keep-out overlap check passed, so the outer NOT correctly failed.

## Open decisions

1. Final list of v1 entity `type` values.
2. Final list of v1 selector `kind` values.
3. Whether templates/macros are part of v1 or deferred.
4. Whether all constraint IDs must be globally unique within a spec.
5. Whether group IDs and constraint IDs share one namespace or separate namespaces.
6. Whether warnings can pass validation while still appearing in evidence.
7. Whether validation result artifacts should become their own public runtime contract.
