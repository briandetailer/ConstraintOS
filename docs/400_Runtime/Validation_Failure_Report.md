# Validation Failure Report

The Validation Failure Report extracts every non-passing validation result into a focused, automation-ready report.

It is not a replacement for the full validation report. It is a smaller view designed for remediation, revision prompts, dashboards, and approval review.

## Purpose

```text
Validation Report
  ↓
Failure Reporter
  ↓
Failure Report
```

## Current behavior

The reporter currently:

- Accepts a `ValidationReport` object or validation report dictionary.
- Includes every result whose status is not `passed`.
- Preserves gate ID, gate name, status, required-pass flag, reason, issue code, severity, and remediation.
- Preserves applied constraint pack references from the validation report.
- Produces a `passed` report when there are no non-passing results.
- Produces a `failed` report when one or more non-passing results are present.

## Example

```json
{
  "failure_report": {
    "id": "FAILURE-REPORT-0001",
    "validation_report_id": "VALIDATION-REPORT-0001",
    "status": "failed",
    "failure_count": 1,
    "constraint_packs": [
      {
        "id": "CPACK-0001",
        "version": "0.1",
        "title": "LF4 Engineering Atlas Constraint Pack"
      }
    ]
  },
  "failures": [
    {
      "gate_id": "GATE-0001",
      "gate_name": "LF4 Specificity Gate",
      "status": "missing_evidence",
      "required_pass": true,
      "reason": "No evidence was supplied for this gate.",
      "issue_code": "VAL-0001",
      "severity": "blocker",
      "remediation": "Supply evidence for the required validation gate."
    }
  ]
}
```

## Design note

This creates the remediation layer that future renderer or prompt-revision systems can consume without needing to understand the full validation report shape. Constraint pack traceability remains visible so remediation can stay tied to the standards that produced the failure.
