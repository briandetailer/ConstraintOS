# Runtime Scheduler

Status: Milestone 2 / Sprint 2

## Purpose
The Runtime Scheduler assigns execution plan nodes to available workers based on plugin capability.

The scheduler does not execute work. It only maps planned nodes to worker IDs.

## Responsibilities

- Consume execution plans from the Runtime Planner.
- Match execution nodes to workers by plugin capability.
- Produce deterministic assignments.
- Report unscheduled nodes when no capable worker exists.

## Non-Responsibilities

- Building execution plans.
- Running plugins.
- Managing worker leases.
- Persisting queue state.
- Validating artifacts.

## Basic Usage

```python
from runtime.planner import RuntimePlanner
from runtime.scheduler import RuntimeScheduler, WorkerCapability

plan = RuntimePlanner().build({
    "execution_steps": [
        {"id": "NODE-0001", "plugin": "blender", "action": "render"},
    ]
})

schedule = RuntimeScheduler().schedule(plan, [
    WorkerCapability("WORKER-0001", ["blender"]),
])
```

## Design Principles

1. Deterministic worker selection.
2. Plugin capability matching.
3. No execution side effects.
4. Partial schedules are explicit.
