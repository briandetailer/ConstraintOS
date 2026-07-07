# Runtime Approval Gate Initial Verifier

## Purpose

This note records the first post-Milestone 3 approval-gate implementation track.

Runtime Milestone 3 is closed. Approval gates are now a separate follow-up track. This keeps approval decisions downstream from execution, validation, and evidence generation.

## Status

Current status:

```text
approval decision verifier, policy verifier, schemas, report writer, evidence-linked helper, and contract registry promotion implemented
```

Implemented modules:

```text
runtime/approval.py
runtime/approval_gate.py
```

Implemented artifact writer:

```text
runtime/artifacts/approval_reporter.py
```

Public exports:

```python
verify_runtime_approval_decision(payload)
verify_runtime_approval_policy(payload)
create_runtime_approval_decision(evidence_manifest_artifact, policy, decided_by, decided_at)
RuntimeApprovalReportWriter
```

Implemented schemas:

```text
schemas/runtime/v1/runtime-approval-decision.schema.json
schemas/runtime/v1/runtime-approval-policy.schema.json
schemas/runtime/v1/runtime-approval-report.schema.json
```

Promoted runtime contracts:

```text
runtime_approval_decision
runtime_approval_policy
runtime_approval_report
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

The policy verifier and schema expect a JSON-style payload with:

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

## Implemented evidence-linked helper behavior

The evidence-linked helper currently:

1. Requires an evidence manifest artifact dictionary.
2. Reads the evidence manifest payload through the artifact metadata path.
3. Verifies the evidence manifest with `verify_runtime_evidence_manifest`.
4. Verifies the approval policy with `verify_runtime_approval_policy`.
5. Produces an approval decision payload.
6. Approves only when both evidence and policy verification pass.
7. Rejects when evidence or policy verification fails.
8. Records approval checks for evidence verification and policy verification.
9. Preserves evidence and policy inputs without mutation.

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

## Implemented policy schema behavior

The approval policy JSON Schema currently checks:

1. Policy payload has all required top-level sections.
2. Policy header includes name, version, and contract registry version.
3. Contract registry version is `runtime-contracts/v1`.
4. Required evidence artifacts include all current Runtime evidence artifact roles.
5. Required checks are non-empty strings.
6. Allowed decisions are constrained to supported decision values.
7. Allowed check statuses are constrained to supported check status values.
8. Approvers are non-empty strings.
9. Waiver rules require `requires_note_or_waived_check: true`.
10. Rejection rules require `requires_note_or_failed_check: true`.
11. Unknown top-level, header, waiver, or rejection fields are rejected.

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

## Implemented contract registry behavior

The runtime contract registry now includes public approval contracts for:

1. `runtime_approval_decision`
2. `runtime_approval_policy`
3. `runtime_approval_report`

The artifact-writer coverage verifier now also requires `RuntimeApprovalReportWriter -> runtime_approval_report`.

## Test files

```text
runtime/tests/test_runtime_approval.py
runtime/tests/test_runtime_approval_gate.py
runtime/tests/test_runtime_approval_contracts.py
```

## Remaining approval-gate work

Recommended next slice:

1. Add approval-gate closeout/status documentation.
