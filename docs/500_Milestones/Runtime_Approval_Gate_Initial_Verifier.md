# Runtime Approval Gate Initial Verifier

## Purpose

This note records the first post-Milestone 3 approval-gate implementation slice.

Runtime Milestone 3 is closed. Approval gates are now a separate follow-up track. This keeps approval decisions downstream from execution, validation, and evidence generation.

## Status

Current status:

```text
initial approval decision verifier implemented
```

Implemented module:

```text
runtime/approval.py
```

Public export:

```python
verify_runtime_approval_decision(payload)
```

## Approval decision payload

The verifier expects a JSON-style payload with:

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

## Implemented verification behavior

The verifier currently checks:

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

## Test file

```text
runtime/tests/test_runtime_approval.py
```

## Remaining approval-gate work

Recommended next slices:

1. Add approval decision JSON Schema.
2. Add approval report artifact writer.
3. Add approval policy object and verifier.
4. Decide when approval contracts should be added to the runtime contract registry.
5. Add evidence-linked approval helpers that consume Runtime evidence manifests without modifying evidence artifacts.
