# Runtime Planner

Status: Milestone 2 / Sprint 1

## Purpose
The Runtime Planner converts a validated ConstraintOS specification or runtime request into a deterministic execution plan.

The planner does not execute work. It only decides what must be done, which plugins are required, and which execution stages can run in order.

## Responsibilities

- Build execution plans from specification-like payloads.
- Normalize steps into execution nodes.
- Preserve explicit dependencies.
- Detect unknown dependencies.
- Detect circular dependencies.
- Group executable nodes into deterministic stages.
- Report required plugins.

## Non-Responsibilities

- Running plugins.
- Scheduling workers.
- Validating rendered outputs.
- Managing user identity.
- Managing billing or tenant boundaries.
- Persisting artifacts.

## Basic Usage

```python
from runtime.planner import RuntimePlanner

plan = RuntimePlanner().build({
    "artifact": {"id": "SPEC-0001"},
    "execution_steps": [
        {"id": "NODE-0001", "plugin": "blender", "action": "render"},
        {"id": "NODE-0002", "plugin": "illustrator", "action": "vectorize", "depends_on": ["NODE-0001"]},
    ],
})

print(plan.to_dict())
```

## Design Principles

1. Deterministic planning.
2. Plugin-agnostic execution modeling.
3. Explicit dependency handling.
4. Immutable plan records.
5. Clear separation between planning, scheduling, execution, and validation.

## Next Work

The scheduler should consume execution plans and assign ready stages to workers.
