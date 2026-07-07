# Runtime Approval Policy Enforcement

## Purpose

This note records the approval-policy enforcement follow-up after the initial Runtime approval CLI and policy examples.

The previous approval policy verifier validated policy shape. This slice adds decision-against-policy enforcement so approval decisions are checked against the specific policy they claim to satisfy.

## Status

Current status:

```text
initial approval decision policy enforcement implemented
```

Implemented module:

```text
runtime/approval.py
```

Public export:

```python
verify_runtime_approval_decision_against_policy(decision, policy)
```

Decision creation integration:

```text
runtime/approval_gate.py
```

## Enforcement behavior

The policy enforcement verifier currently checks:

1. Approval decision payload is valid.
2. Approval policy payload is valid.
3. Decision `approval_policy` matches the policy name.
4. Decision `decided_by` is listed in policy approvers.
5. Decision value is allowed by the policy.
6. Required policy checks are present in decision check sources.
7. Check statuses are allowed by the policy.

## Decision creation behavior

`create_runtime_approval_decision` now enforces the generated decision against the supplied policy.

If the generated decision does not satisfy the policy, the helper:

1. Sets the approval decision to `rejected`.
2. Adds a failed policy-enforcement approval check.
3. Adds policy-enforcement issues to approval notes.
4. Keeps the generated decision payload structurally valid.

## Test file

```text
runtime/tests/test_runtime_approval_policy_enforcement.py
```

## Validation target

Expected test delta from the previous 468-pass baseline:

```text
+5 tests
```

Expected full-suite baseline after validation:

```text
473 passed
```
