# Runtime Architecture Status

## Purpose

The Runtime layer turns a runtime specification into an auditable execution result. It is intentionally deterministic at the orchestration boundary so that planner output, scheduler output, execution IDs, events, artifacts, final reports, contract registries, and evidence manifests can be inspected and tested.

The Runtime layer should be understood as part of a broader generation-validation architecture rather than as a better prompting layer. The long-term boundary is:

```text
specification -> planning -> execution -> independent validation -> evidence -> approval
```

Execution may be nondeterministic. Validation and evidence must remain independently inspectable.

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

## Public contract and evidence posture

Milestone 3 has expanded the runtime beyond core orchestration into public evidence boundaries:

- runtime result reports
- runtime trace reports
- runtime evidence manifests
- runtime contract registry reports
- replay verifiers
- trace verifiers
- contract registry verifiers
- artifact writer contract coverage verification
- self-contained evidence bundles

The Python runtime may remain the implementation core, but adoption should be based on portable JSON artifacts and versioned contracts so non-Python consumers can integrate through Node.js, .NET, Terraform, CI/CD, or audit tooling.

## Validation principles

Generation must not self-certify. Runtime validation should remain independent of execution, and approval should remain a distinct downstream boundary. See `Runtime_Generation_Validation_Principles.md` for the active design principles governing future runtime, CSL, validator, and enterprise-boundary work.

## Current baseline

Last user-reported full-suite baseline before Runtime Milestone 3 closeout documentation: 398 passing tests.

The later CSL validation-result contract work is adjacent groundwork and should be validated separately before treating the whole branch as a newer baseline.

## Closeout posture

Runtime Milestone 3 is now in closeout and external-consumer packaging mode. See `Runtime_Milestone_3_Closeout.md` for the closeout record.

The next Runtime work should focus on examples, documentation, and integration boundaries for the public evidence package rather than additional core orchestration implementation.

CSL design and early verifier work is parked as future-facing schema/compiler/validator groundwork and should resume as a dedicated track after Runtime Milestone 3 is closed.
