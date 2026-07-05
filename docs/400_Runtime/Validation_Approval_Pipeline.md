# Validation Approval Pipeline

The Validation Approval Pipeline runs validation, builds a focused failure report, and then applies approval policy.

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
Failure Report
  ↓
Approval Engine
  ↓
Approval Decision
```

## Purpose

The pipeline exists so callers do not need to manually wire the Validation Kernel, Failure Reporter, and Approval Engine together.

It keeps the concerns separated while still providing one deterministic operation:

```text
Evaluate this artifact candidate against this render specification and decide whether it is approved.
```

## Current behavior

The pipeline currently supports render specifications directly:

- Reads `validation.gates` from the render specification.
- Evaluates supplied evidence against those gates.
- Produces a validation report.
- Produces a focused failure report from any non-passing validation results.
- Applies approval policy.
- Returns all outputs together.

## Result shape

```json
{
  "validation": {
    "validation_report": {
      "id": "VALIDATION-REPORT-0001",
      "subject_id": "LF4-ENGINE",
      "status": "failed"
    },
    "results": []
  },
  "failure_report": {
    "failure_report": {
      "id": "FAILURE-REPORT-0001",
      "status": "failed",
      "failure_count": 1
    },
    "failures": []
  },
  "approval": {
    "approval": {
      "id": "APPROVAL-0001",
      "status": "rejected"
    },
    "decision": {
      "summary": "Rejected because required validation gates did not pass.",
      "reasons": []
    }
  }
}
```

## Design note

This pipeline still does not perform image inspection. It is the orchestration layer that future validators will use once visual, geometry, reference-image, or renderer-specific evidence is available.
