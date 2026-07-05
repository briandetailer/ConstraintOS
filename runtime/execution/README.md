# Runtime Execution

Status: Milestone 2 / Sprint 3

## Purpose
The execution layer consumes scheduled assignments and produces execution results.

Sprint 3 introduces a dry-run executor. It simulates assignments without invoking external renderer processes.

## Responsibilities

- Accept execution requests.
- Simulate scheduled assignments.
- Produce per-node execution results.
- Preserve request/result traceability.
- Reject requests that are not dry-run requests.

## Boundaries

The execution layer does not call renderer applications yet. Renderer application calls belong to future plugin work.

## Basic Usage

```python
from runtime.execution import DryRunExecutor, ExecutionRequest

request = ExecutionRequest(
    id="EXEC-REQ-0001",
    schedule_id="SCHEDULE-0001",
    assignments=[
        {"node_id": "NODE-0001", "worker_id": "WORKER-0001", "plugin": "blender", "action": "render"}
    ],
)

result = DryRunExecutor().execute(request)
```

## Design Principles

1. Execution is explicit.
2. Dry-run execution must be safe.
3. Results must be structured and traceable.
