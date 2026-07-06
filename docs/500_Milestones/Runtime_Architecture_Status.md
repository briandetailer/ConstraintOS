# Runtime Architecture Status

## Purpose

The Runtime layer turns a runtime specification into an auditable execution result. It is intentionally deterministic at the orchestration boundary so that planner output, scheduler output, execution IDs, events, artifacts, and final reports can be inspected and tested.

## Runtime package map

```text
runtime/
  artifacts/     artifact store, collector, and report writer
  execution/     execution request/result models and executors
  planner/       runtime planning and dependency validation
  scheduler/     worker capabilities and stage scheduling
  tests/         runtime unit and integration tests
  context.py     runtime execution context
  engine.py      orchestration entry point
  events.py      runtime event model
  result.py      top-level runtime result model
  state.py       runtime lifecycle state model
```

## Orchestration sequence

```text
RuntimeEngine.run
  1. Create runtime_started event.
  2. Build plan from specification.
  3. Validate dependencies.
  4. Create runtime_planned event.
  5. Schedule nodes against worker capabilities.
  6. Create runtime_scheduled event.
  7. Stop early when schedule is partial.
  8. Build ExecutionRequest from schedule.
  9. Create runtime_execution_started event.
  10. Execute request.
  11. Collect artifacts.
  12. Create runtime_completed event.
  13. Return RuntimeResult.
```

## RuntimeResult contract

RuntimeResult provides:

- runtime id
- runtime status
- success flag
- terminal helper
- successful helper
- plan payload
- schedule payload
- execution payload
- artifact payload
- event list
- messages
- summary counts

The serialized runtime_result payload includes:

- id
- status
- success
- terminal
- successful
- created

## Event contract summary

### runtime_started

Includes runtime id and runtime context.

### runtime_planned

Includes plan id.

### runtime_scheduled

Includes schedule id and schedule status.

### runtime_execution_started

Includes schedule id and execution request id.

### runtime_completed

Includes execution result id, execution status, node result count, and artifact count.

### runtime_failed

For partial schedules, includes unscheduled nodes and unscheduled count.

For defensive exception-boundary failures, includes error text and error type.

## Current baseline

Current validated baseline: 355 passing tests.

## Closeout posture

The Runtime layer is complete enough to close Milestone 2. Future Runtime work should be framed as contract hardening, replayability, plugin interface work, or integration with traceability/provenance rather than as core Milestone 2 implementation.
