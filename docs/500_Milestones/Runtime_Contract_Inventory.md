# Runtime Contract Inventory

## Purpose

Milestone 3 starts by inventorying the Runtime contract boundaries before adding formal schemas, replay verification, or provenance integration.

This document is intentionally descriptive. It does not introduce JSON Schema files, validation classes, or source-code changes. Its job is to define the current contract surfaces that future Milestone 3 slices should harden in small, test-backed increments.

## Baseline

Runtime Milestone 2 is complete with the last locally validated full-suite baseline reported as:

```text
355 passed
```

The current Runtime flow is:

```text
specification -> planner -> dependency validation -> scheduler -> execution request -> executor -> artifact collection -> runtime result
```

## Contract inventory status

| Contract area | Current owner | Current form | Milestone 3 hardening target |
| --- | --- | --- | --- |
| Runtime input specification | `runtime/planner/planner.py` | flexible dictionary input | documented required/optional fields, explicit validation, stable error behavior |
| Execution plan | `runtime/planner/models.py` | `ExecutionPlan.to_dict()` payload | schema-backed plan contract and replay consistency checks |
| Dependency validation | `runtime/planner/planner.py` and `DependencyResolver` | planner and resolver validation | audit-friendly dependency validation results |
| Schedule result | `runtime/scheduler/models.py` | `ScheduleResult.to_dict()` payload | schema-backed schedule contract and deterministic assignment checks |
| Execution request | `runtime/execution/models.py` | `ExecutionRequest.from_schedule(...)` and `to_dict()` | strict request derivation from scheduled runtime output |
| Execution result | `runtime/execution/models.py` | `ExecutionResult.to_dict()` payload | executor result validation and malformed-output protection |
| Plugin executor boundary | `runtime/execution/protocols.py`, `runtime/execution/plugin_executor.py`, `runtime/plugins/base.py` | protocol plus plugin result model | plugin input/result contract validation |
| Runtime event stream | `runtime/events.py` | ordered `RuntimeEvent` list | replay verifier for event order, payload requirements, and terminal state alignment |
| Runtime artifacts | `runtime/artifacts/` | artifact ledger and collector | artifact-to-node and artifact-to-output traceability |
| Runtime result | `runtime/result.py` | top-level `RuntimeResult.to_dict()` payload | schema-backed runtime result and summary consistency checks |
| Runtime report | `runtime/artifacts/reporter.py` | JSON snapshot artifact | stable report contract and generated report acceptance example |
| CLI runtime output | `runtime_cli.py` | text/JSON/output-file/report modes | CLI acceptance examples mapped to runtime report output |

## Runtime input specification

### Current contract

The planner accepts a dictionary specification and derives a source id from the first nested object with an `id` under one of these keys:

```text
artifact
specification
runtime_job
execution_request
```

The planner extracts steps from one of these step lists:

```text
execution_steps
steps
runtime_steps
```

The planner also supports compatibility fallbacks for `render_job` and `artifact` shaped inputs.

Each execution step currently contributes:

- node id
- plugin or renderer
- action
- inputs
- outputs
- depends_on

### Milestone 3 target

Add an explicit runtime input contract that preserves the current compatibility paths while making the preferred specification shape clear. Future validation should reject malformed inputs with deterministic error messages and should preserve existing accepted inputs unless a migration document says otherwise.

## Execution plan contract

### Current contract

The execution plan serializes as:

- `execution_plan` metadata
- `required_plugins`
- `stages`
- `nodes`
- `dependencies`
- `messages`

The plan metadata includes:

- id
- source id
- status
- created date

Nodes include:

- id
- plugin
- action
- inputs
- outputs

Dependencies include:

- node id
- depends on

Stages include:

- stage id
- node ids

### Milestone 3 target

Add plan contract tests that verify:

- every dependency references known nodes
- every stage references known nodes
- every node appears in exactly one stage
- stage ordering respects dependency ordering
- required plugin list matches plan nodes
- plan id and source id remain deterministic for deterministic input

## Schedule result contract

### Current contract

The schedule result serializes as:

- `schedule_result` metadata
- `assignments`
- `unscheduled_nodes`
- `messages`

Schedule metadata includes:

- id
- plan id
- status
- created date

Assignments include:

- node id
- stage id
- worker id
- plugin
- action

### Milestone 3 target

Add schedule contract tests that verify:

- every assignment references a planned node
- assigned plugin and action match the plan node
- assigned stage matches the plan stage
- workers support assigned plugins
- unavailable workers are not assigned
- the same worker is not double-booked within the same stage
- partial schedules preserve unscheduled nodes and stop before execution

## Execution request contract

### Current contract

Execution requests are derived from scheduled runtime output through `ExecutionRequest.from_schedule(...)`.

The execution request serializes as:

- `execution_request` metadata
- `assignments`

Execution request metadata includes:

- id
- schedule id
- dry-run flag
- created date

The Runtime engine currently derives deterministic runtime execution request ids in this pattern:

```text
RUNTIME-0001-EXEC-REQ-0001
```

### Milestone 3 target

Add request contract tests that verify:

- requests cannot be built from partial schedules unless explicitly allowed
- request schedule id matches the schedule result id
- request assignments match scheduled assignments after runtime enrichment
- node inputs and outputs are carried into execution assignments
- deterministic runtime request ids remain stable

## Execution result contract

### Current contract

Execution results serialize as:

- `execution_result` metadata
- `node_results`
- `messages`

Execution result metadata includes:

- id
- request id
- status
- created date

Node results include:

- node id
- worker id
- plugin
- action
- status
- outputs
- message

The Runtime engine currently derives deterministic runtime execution result ids in this pattern:

```text
RUNTIME-0001-EXEC-RESULT-0001
```

### Milestone 3 target

Add execution result contract tests that verify:

- result request id matches execution request id
- every node result references a requested assignment
- node result plugin/action/worker values remain aligned with the assignment
- execution status matches node result completeness
- malformed executor output cannot break Runtime result assembly

## Plugin executor boundary

### Current contract

Runtime executors implement an `execute(...)` interface that accepts an `ExecutionRequest` or dictionary request and returns an `ExecutionResult`.

Runtime plugins expose:

- name
- capabilities
- execute assignment behavior

Plugin results include:

- plugin
- node id
- action
- status
- outputs
- artifacts
- logs
- metrics

The plugin executor maps plugin results into node execution results.

### Milestone 3 target

Add plugin boundary tests that verify:

- plugins must return the expected plugin result shape
- missing plugin result fields are handled predictably
- plugin artifacts are preserved or intentionally mapped
- plugin logs are preserved in node result messages
- plugin errors become runtime-safe failures rather than unhandled crashes

## Runtime event stream contract

### Current contract

Runtime events serialize as:

- timestamp
- event type
- payload

Current event types are:

```text
runtime_started
runtime_planned
runtime_scheduled
runtime_execution_started
runtime_completed
runtime_failed
```

Successful runs should follow this order:

```text
runtime_started -> runtime_planned -> runtime_scheduled -> runtime_execution_started -> runtime_completed
```

Partial schedule runs should follow this order:

```text
runtime_started -> runtime_planned -> runtime_scheduled -> runtime_failed
```

Exception-boundary failures should include a `runtime_failed` event with error text and error type.

### Milestone 3 target

Add a replay or audit verifier that checks:

- event ordering
- required payload keys per event type
- event ids and referenced ids match plan, schedule, execution request, and execution result payloads
- terminal runtime status matches the final event path
- partial schedule failure includes unscheduled node details
- exception failure includes error text and error type

## Runtime artifact contract

### Current contract

Runtime artifacts serialize as:

- id
- uri
- kind
- producer
- metadata

The artifact store serializes as:

- `artifact_store` metadata
- `artifacts`

Artifact store metadata includes:

- root
- count

The current default artifact id sequence is:

```text
ARTIFACT-0001
```

### Milestone 3 target

Add artifact traceability checks that verify:

- every artifact id is unique
- artifact count matches serialized artifact entries
- artifact producer maps to a runtime id, execution result id, node id, or report writer role
- execution outputs that represent artifacts can be traced to artifact records
- runtime reports are marked with the `runtime_report` artifact role

## Runtime result contract

### Current contract

Runtime results serialize as:

- `runtime_result` metadata
- `summary`
- `plan`
- `schedule`
- `execution`
- `events`
- `messages`
- `artifacts`, when present

Runtime result metadata includes:

- id
- status
- success
- terminal
- successful
- created date

Runtime result summary includes counts for:

- plan nodes
- plan stages
- scheduled assignments
- unscheduled nodes
- node results
- artifacts
- events

### Milestone 3 target

Add runtime result contract tests that verify:

- `terminal` and `successful` align with runtime state semantics
- summary counts match the serialized payloads
- completed runtime results include execution and artifacts
- partial schedule runtime results omit execution and preserve schedule failure details
- failed runtime results preserve the best available partial payloads

## Runtime report contract

### Current contract

Runtime reports are JSON snapshots of runtime result payloads written as artifacts. Report metadata includes:

- content type
- runtime id
- runtime status
- runtime success
- summary
- artifact role

### Milestone 3 target

Add report contract tests and examples that verify:

- report JSON matches `RuntimeResult.to_dict()` output
- report artifact metadata mirrors runtime result status and summary
- generated report paths are deterministic for deterministic runtime ids
- CLI report generation produces the same report contract as direct runtime report writing

## Provenance and traceability integration target

Milestone 3 should connect Runtime output to provenance or traceability records without weakening deterministic runtime behavior.

The initial integration target should preserve these identifiers across layers:

- runtime result id
- plan id
- schedule id
- execution request id
- execution result id
- node ids
- worker ids
- artifact ids

The first traceability mapping should be read-only or generated from existing Runtime output. It should not require Runtime execution to depend on provenance storage.

## Acceptance-level examples to add later in Milestone 3

Future Milestone 3 examples should cover:

- complete deterministic workflow
- CLI-driven runtime execution
- generated runtime report
- failure or partial schedule audit
- malformed plugin output protection
- runtime result to traceability record mapping

## Recommended next green slices

1. Add a Runtime contract inventory test or documentation link check, if the repository has an existing docs validation pattern.
2. Add a small replay verifier focused only on successful runtime event order.
3. Add replay verifier tests for partial schedule event order and payload requirements.
4. Add deterministic id consistency checks across runtime result payloads.
5. Add plugin executor malformed-output protection with focused tests.
6. Add runtime report contract tests.
7. Add provenance or traceability mapping as a pure adapter over `RuntimeResult.to_dict()`.

## Validation

This slice is documentation-only. The expected full-suite result should remain:

```text
355 passed
```

Recommended validation command from the repository root:

```powershell
git pull
.\.venv\Scripts\python.exe -m pytest
```
