# Runtime Architecture Status

## Purpose

The Runtime layer turns a runtime specification into an auditable execution result. It is intentionally deterministic at the orchestration boundary so that planner output, scheduler output, execution IDs, events, artifacts, final reports, contract registries, evidence manifests, CLI summaries, and JSON Schema validation can be inspected and tested.

The Runtime layer should be understood as part of a broader generation-validation architecture rather than as a better prompting layer. The long-term boundary is:

```text
specification -> planning -> execution -> independent validation -> evidence -> approval
```

Execution may be nondeterministic. Validation, evidence, and approval boundaries must remain independently inspectable.

## Runtime package map

```text
runtime/
  artifacts/     artifact store, collector, report writers, and evidence writers
  execution/     execution request/result models and executors
  planner/       runtime planning and dependency validation
  scheduler/     worker capabilities and stage scheduling
  tests/         runtime unit and integration tests
  context.py     runtime execution context
  contracts.py   public runtime contract registry and contract verifiers
  engine.py      orchestration entry point
  events.py      runtime event model
  replay.py      runtime event replay and consistency verification
  result.py      top-level runtime result model
  state.py       runtime lifecycle state model
  traceability.py runtime trace adapter and trace verification
  cli.py         runtime evidence package CLI entry point
  __main__.py    runtime module CLI dispatcher
```

## Schema package map

```text
schemas/runtime/v1/
  runtime-result.schema.json
  runtime-report.schema.json
  runtime-traceability.schema.json
  runtime-trace-report.schema.json
  runtime-evidence-manifest.schema.json
  runtime-contract-registry.schema.json
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

The public JSON Schema for this boundary is `schemas/runtime/v1/runtime-result.schema.json`.

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

## Public contract and evidence posture

Milestone 3 expanded the runtime beyond core orchestration into public evidence boundaries:

- runtime result reports
- runtime trace reports
- runtime evidence manifests
- runtime contract registry reports
- replay verifiers
- trace verifiers
- contract registry verifiers
- artifact writer contract coverage verification
- self-contained evidence bundles
- runtime evidence CLI entry points
- public Runtime JSON Schemas

The Python runtime may remain the implementation core, but adoption should be based on portable JSON artifacts, versioned contracts, CLI generation, and JSON Schema validation so non-Python consumers can integrate through Node.js, .NET, Terraform, CI/CD, or audit tooling.

## Validation principles

Generation must not self-certify. Runtime validation should remain independent of execution, evidence should remain inspectable, and approval should remain a distinct downstream boundary. See `Runtime_Generation_Validation_Principles.md` and `Runtime_Approval_Gate_Target.md` for the active design principles governing future runtime, CSL, validator, and enterprise-boundary work.

## Current baseline

Current user-reported full-suite baseline: 425 passing tests.

## Closeout posture

Runtime Milestone 3 is complete from the Runtime evidence, contract, CLI, and JSON Schema perspective. See `Runtime_Milestone_3_Closeout.md` for the closeout record.

Approval gates remain a valid follow-up boundary, but they should not block Runtime Milestone 3 closeout.

CSL design and early verifier work is parked as future-facing schema/compiler/validator groundwork and should resume as a dedicated track after Runtime Milestone 3 is closed.
