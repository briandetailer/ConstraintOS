# Validation Kernel

The Validation Kernel evaluates whether a produced artifact has evidence for every required validation gate.

This is intentionally separate from rendering. Renderers produce candidate outputs; validators decide whether those outputs satisfy the contract.

## Purpose

The kernel converts validation gates and evidence into a structured validation report.

```text
Render Specification
  ↓
Validation Gates
  ↓
Evidence
  ↓
Validation Kernel
  ↓
Validation Report
```

## Current behavior

The first implementation supports deterministic gate evaluation:

- A required gate passes only when supplied evidence has a passing status.
- A required gate fails when evidence is missing or failing.
- An optional gate can fail without failing the whole report.
- Render specifications can be evaluated directly by reading their `validation.gates` section.
- Evidence must reference known gates from the evaluated specification.
- Evidence may only be supplied once per gate.
- Missing or failing evidence receives a machine-readable issue code.
- Applied constraint pack references are preserved in the validation report.
- Malformed constraint pack references are rejected instead of silently dropped.

## Passing evidence statuses

The kernel currently treats these evidence statuses as passing:

```text
pass
passed
complete
approved
```

## Evidence alignment

Evidence is validated against the gate set before any report is produced.

The kernel rejects:

- evidence for a gate that is not present in the evaluated gate list
- duplicate evidence entries for the same gate

This prevents silent overwrites and prevents unrelated evidence from being ignored.

## Constraint pack traceability

When a render specification contains `constraint_packs`, the validation report records those references under `validation_report.constraint_packs`.

Each reference must be an object with an `id`; malformed references are rejected before a validation report is produced.

This keeps the validation result tied to the reusable standards that were applied before validation.

## Issue codes

Issue codes make validation results usable by automation. A human-readable reason explains the result, while the issue code gives downstream tools a stable remediation target.

Current built-in issue codes:

| Code | Title | Severity | Remediation |
| --- | --- | --- | --- |
| `VAL-0001` | Missing validation evidence | blocker | Supply evidence for the required validation gate. |
| `VAL-0002` | Validation evidence did not pass | blocker | Revise the artifact or provide corrected validation evidence. |

## Example result

```json
{
  "validation_report": {
    "id": "VALIDATION-REPORT-0001",
    "subject_id": "LF4-ENGINE",
    "status": "failed",
    "constraint_packs": [
      {
        "id": "CPACK-0001",
        "version": "0.1",
        "title": "LF4 Engineering Atlas Constraint Pack"
      }
    ]
  },
  "results": [
    {
      "gate_id": "GATE-0001",
      "name": "LF4 Specificity Gate",
      "status": "missing_evidence",
      "required_pass": true,
      "reason": "No evidence was supplied for this gate.",
      "issue_code": {
        "code": "VAL-0001",
        "title": "Missing validation evidence",
        "severity": "blocker",
        "remediation": "Supply evidence for the required validation gate."
      }
    }
  ]
}
```

## Design note

This does not yet inspect images or generated files. It defines the reporting structure, pass/fail semantics, traceability metadata, evidence alignment rules, and machine-readable issue codes that future validators will use.
