# Milestone: Root Constraint Pack Audit Header

Status: closed.

## Goal

Combined validation approval results should expose the applied Constraint Pack references at the root of the payload, while still preserving those references inside every generated report and decision.

This gives downstream tools one stable audit header without forcing them to inspect every nested object first.

## Current guarantees

- `ValidationApprovalResult` serializes root-level `constraint_packs`.
- The root audit header is copied from the validation report's applied pack references.
- The root audit header is present when packs are applied.
- The root audit header is an empty list when no packs are applied.
- Nested traceability is still preserved in validation, failure report, remediation plan, revision request, and approval decision outputs.
- `cos-validate` text summaries prefer the root audit header for the Constraint Pack count, with the nested validation report as a fallback.

## Result boundary

```text
Applied Constraint Packs
  ↓
Validation Report Traceability
  ↓
Validation Approval Result Root Audit Header
  ↓
CLI / JSON / Text Consumers
```

## Out of scope

This milestone does not create a full provenance manifest. It only adds the root audit header for applied Constraint Pack references in the combined validation approval result.
