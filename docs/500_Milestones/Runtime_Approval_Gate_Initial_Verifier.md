# Runtime Approval Gate Initial Verifier

## Purpose

This note records the first post-Milestone 3 approval-gate implementation track.

Runtime Milestone 3 is closed. Approval gates are now a separate follow-up track. This keeps approval decisions downstream from execution, validation, and evidence generation.

## Status

Current status:

```text
approval decision verifier, schemas, report writer, and policy verifier implemented
```

Implemented module:

```text
runtime/approval.py
```

Implemented artifact writer:

```text
runtime/artifacts/approval_reporter.py
```

Public exports:

```python
verify_runtime_approval_decision(payload)
verify_runtime_approval_policy(payload)
RuntimeApprovalReportWriter
```

Implemented schemas:

```text
schemas/runtime/v1/runtime-approval-decision.schema.json
schemas/runtime/v1/runtime-approval-report.schema.json
```

## Approval decision payload

The verifier and schema expect a JSON-style payload with:

```text
runtime_approval
checks
notes
```

Required approval fields:

- `runtime_id`
- `evidence_manifest_artifact_id`
- `decision`
- `decided_by`
- `decided_at`
- `approval_policy`

Allowed decisions:

- `approved`
- `rejected`
- `needs_review`
- `waived`

## Approval policy payload

The policy verifier expects a JSON-style payload with:

```text
runtime_approval_policy
required_evidence_artifacts
required_checks
allowed_decisions
allowed_check_statuses
approvers
waiver_rules
rejection_rules
```

Required policy header fields:

- `name`
- `version`
- `contract_registry_version`

Required Runtime evidence artifact roles:

- `runtime_report`
- `runtime_trace_report`
- `runtime_contract_registry`
- `runtime_evidence_manifest`

## Approval checks

Approval checks may record policy-level checks over the evidence package.

Required check fields:

- `id`
- `name`
- `status`
- `source`

Allowed check statuses:

- `passed`
- `failed`
- `waived`
- `needs_review`

Optional check fields:

- `message`
- `metadata`

## Implemented decision verification behavior

The decision verifier currently checks:

1. Approval payload must be a dictionary.
2. Approval header must include required fields.
3. Decision value must be one of the allowed decisions.
4. Checks must be a list.
5. Notes must be a list of non-empty strings.
6. Each check must be a dictionary.
7. Each check must include required check fields.
8. Check status must be one of the allowed statuses.
9. Check message, when present, must be a string.
10. Check metadata, when present, must be a dictionary.
11. Rejected decisions require a failed check or note.
12. Waived decisions require a waived check or note.
13. Verification does not mutate the supplied approval payload.

## Implemented policy verification behavior

The policy verifier currently checks:

1. Policy payload must be a dictionary.
2. Policy header must include required fields.
3. Required evidence artifacts must be a non-empty string list.
4. Required checks must be a non-empty string list.
5. Allowed decisions must be a non-empty string list using supported decision values.
6. Allowed check statuses must be a non-empty string list using supported check status values.
7. Approvers must be a non-empty string list.
8. The policy requires all current Runtime evidence artifact roles.
9. Waiver rules require `requires_note_or_waived_check: true`.
10. Rejection rules require `requires_note_or_failed_check: true`.
11. Verification does not mutate the supplied policy payload.

## Implemented decision schema behavior

The approval decision JSON Schema currently checks:

1. Approval payload has `runtime_approval`, `checks`, and `notes`.
2. Approval header includes all required fields.
3. Decision values are constrained to the allowed enum.
4. Checks are arrays of approval check objects.
5. Check statuses are constrained to the allowed enum.
6. Check metadata, when present, is an object.
7. Notes are arrays of non-empty strings.
8. Unknown top-level, approval, or check fields are rejected.

Semantic checks that JSON Schema cannot express cleanly, such as rejected decisions requiring a failed check or note, remain in the Python verifier.

## Implemented report writer behavior

The approval report writer currently:

1. Requires a valid approval decision before writing.
2. Persists the approval decision JSON payload unchanged.
3. Writes to `approvals/{runtime_id}.json` by default.
4. Registers a `runtime_approval_report` artifact.
5. Records runtime id, evidence manifest artifact id, decision, policy, decider, and decision timestamp as artifact metadata.
6. Does not modify runtime reports, trace reports, evidence manifests, or contract registries.

## Implemented report schema behavior

The approval report JSON Schema currently checks:

1. Artifact id is present.
2. Artifact URI is present.
3. Artifact kind is `file`.
4. Artifact role is `runtime_approval_report`.
5. Content type is `application/json`.
6. Runtime id is present.
7. Evidence manifest artifact id is present.
8. Decision metadata is constrained to the allowed enum.
9. Approval policy, decider, and decision timestamp are present.
10. Unknown artifact or metadata fields are rejected.

## Test file

```text
runtime/tests/test_runtime_approval.py
```

## Remaining approval-gate work

Recommended next slices:

1. Add approval policy JSON Schema.
2. Decide when approval contracts should be added to the runtime contract registry.
3. Add evidence-linked approval helpers that consume Runtime evidence manifests without modifying evidence artifacts.
