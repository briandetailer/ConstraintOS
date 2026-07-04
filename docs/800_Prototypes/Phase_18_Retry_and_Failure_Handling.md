# Phase 18: Retry Policy and Failure Handling

Status: Complete Baseline
Version: 1.0.0-alpha.18

## Purpose
Phase 18 introduces retry policy and failed-job handling. Runtime failures can now be classified, evaluated against retry policy, and converted into structured failed-job records.

## Implemented Scope

- Retry policy module
- Retry policy model
- Retry decision model
- Failed job record model
- Failure classification
- Retry decision logic
- Failed job creation helper
- Retry policy schema
- Retry decision schema
- Failed job schema
- Retry tests
- Retry examples
- Validation support for retry artifacts
- Package version bumped to `1.0.0-alpha.18`

## Failure Handling Philosophy

Failures should become structured system knowledge. The runtime must distinguish between transient failures, missing inputs, validation failures, and configuration problems.

## Failure Classes

- unsupported_job_type
- missing_input
- validation_failure
- runtime_failure

## Retry Rules

1. Only retry statuses named in the policy are retryable.
2. Unsupported job types are not retried automatically.
3. Jobs that reach maximum attempts are moved to structured failed-job records.
4. Retry decisions must be explicit and auditable.
5. Retry policy belongs to runtime coordination, not kernel correctness.

## Recommended Phase 19

Phase 19 should introduce worker heartbeat and job leasing:

1. Worker heartbeat schema
2. Lease record model
3. Lease acquisition helper
4. Lease expiration decision
5. Worker availability tests
6. Runtime coordination documentation
