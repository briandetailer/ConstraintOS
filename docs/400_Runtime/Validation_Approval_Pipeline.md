# Validation Approval Pipeline

The Validation Approval Pipeline runs validation and then applies approval policy to the validation report.

It is the first combined workflow for the post-render side of ConstraintOS.

```text
Render Specification
  ↓
Validation Evidence
  ↓
Validation Kernel
  ↓
Validation Report
  ↓
Approval Engine
  ↓
Approval Decision
```

## Purpose

The pipeline exists so callers do not need to manually wire the Validation Kernel and Approval Engine together.

It keeps the concerns separated while still providing one deterministic operation:

```text
Evaluate this artifact candidate against this render specification and decide whether it is approved.
```

## Current behavior

The pipeline currently supports render specifications directly:

- Reads `validation.gates` from the render specification.
- Evaluates supplied evidence against those gates.
- Produces a validation report.
- Applies approval policy.
- Returns both outputs together.

## Result shape

```json
{
  "validation": {
    "validation_report": {
      "id": "VALIDATION-REPORT-0001",
      "subject_id": "LF4-ENGINE",
      "status": "passed"
    },
    "results": []
  },
  "approval": {
    "approval": {
      "id": "APPROVAL-0001",
      "status": "approved"
    },
    "decision": {
      "summary": "Approved because all validation gates passed.",
      "reasons": []
    }
  }
}
```

## Design note

This pipeline still does not perform image inspection. It is the orchestration layer that future validators will use once visual, geometry, reference-image, or renderer-specific evidence is available.
