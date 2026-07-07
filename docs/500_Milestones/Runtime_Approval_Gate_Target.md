# Runtime Approval Gate Target

## Purpose

This document defines the post-Milestone 3 target for approval-gate contracts.

Milestone 3 established that validation is independent of execution. The next boundary is approval: a runtime can pass structural validation and still require human, business, regulatory, security, or domain-specific approval before the output is accepted.

Approval must remain a separate downstream decision rather than being hidden inside execution, validation, or evidence generation.

## Status

Current status:

```text
target defined / approval gate contracts not yet implemented
```

Milestone 3 Runtime evidence can prove what happened and whether contract/evidence verification passed. It does not yet model a separate approval decision.

## Boundary distinction

Runtime execution answers:

```text
Did the requested runtime workflow execute?
```

Runtime validation answers:

```text
Does the generated evidence satisfy the expected contracts and checks?
```

Approval answers:

```text
Should this result be accepted for its business, engineering, compliance, or release purpose?
```

These are related but not interchangeable.

## Approval gate position

The long-term pipeline should preserve this boundary:

```text
specification -> planning -> execution -> independent validation -> evidence -> approval
```

Approval consumes evidence. It should not rewrite or silently reinterpret the evidence package.

## Proposed approval decision contract

A future approval decision payload should be JSON-first and externally inspectable.

Minimum shape:

```json
{
  "runtime_approval": {
    "runtime_id": "RUNTIME-0001",
    "evidence_manifest_artifact_id": "ARTIFACT-0004",
    "decision": "approved",
    "decided_by": "user-or-system-id",
    "decided_at": "2026-07-06T00:00:00Z",
    "approval_policy": "default-runtime-approval/v1"
  },
  "checks": [],
  "notes": []
}
```

## Decision values

Initial decision values should be:

- `approved`
- `rejected`
- `needs_review`
- `waived`

### approved

The evidence package is accepted for the target use case.

### rejected

The evidence package is not accepted. Rejection should include at least one check or note explaining why.

### needs_review

The evidence package is structurally present but requires further human/domain review before acceptance.

### waived

A policy owner accepted the result despite one or more issues. Waivers must preserve who waived the issue, why, and under which policy.

## Approval check record

Approval checks should record policy-level decisions without duplicating the full evidence payload.

Example:

```json
{
  "id": "APPROVAL-CHECK-0001",
  "name": "runtime evidence manifest verified",
  "status": "passed",
  "source": "verify_runtime_evidence_manifest",
  "message": "Evidence manifest verification passed."
}
```

Expected check fields:

| Field | Required | Purpose |
| --- | --- | --- |
| `id` | yes | Stable approval check id. |
| `name` | yes | Human-readable check name. |
| `status` | yes | `passed`, `failed`, `waived`, or `needs_review`. |
| `source` | yes | Tool, policy, verifier, or reviewer that produced the check. |
| `message` | no | Human-readable explanation. |
| `metadata` | no | Optional domain-specific context. |

## Approval policy record

A future approval gate should support named approval policies.

Example policy names:

- `default-runtime-approval/v1`
- `ci-runtime-approval/v1`
- `manual-engineering-review/v1`
- `regulated-release-approval/v1`

Policies should define:

- required evidence artifacts
- required contract registry version
- required validation checks
- who or what may approve
- waiver rules
- rejection rules

## Evidence linkage requirements

An approval decision should link to evidence, not merely runtime ids.

Required links:

- runtime id
- evidence manifest artifact id
- contract registry version

Optional links:

- runtime report artifact id
- trace report artifact id
- contract registry artifact id
- approval policy artifact id

## What approval must not do

Approval must not:

- mutate the runtime report
- mutate the trace report
- mutate the evidence manifest
- silently override failed validation
- replace manifest verification
- hide waiver reasons
- collapse business acceptance into runtime success

## Future public contracts

Approval should likely introduce these public contracts:

- `runtime_approval_decision`
- `runtime_approval_policy`
- `runtime_approval_report`

These should be added to the runtime contract registry only after their object shapes and tests are defined.

## Verification strategy

Approval-gate implementation should be test-backed.

Tests should verify:

1. Approval decisions require runtime id and evidence manifest reference.
2. Decision values are constrained to the approved enum.
3. Rejections require notes or failed checks.
4. Waivers require waiver reason and deciding authority.
5. Approval does not alter evidence artifacts.
6. Approval policy version is recorded.
7. Approval reports can be consumed without Python imports.

## Milestone 3 disposition

This target does not block Runtime Milestone 3 closeout.

It should be treated as a dedicated approval-boundary follow-up after Runtime Milestone 3 closes.
