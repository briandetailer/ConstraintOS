# Validation CLI

`cos-validate` runs the validation approval pipeline from the command line.

It evaluates a render specification against supplied validation evidence, then produces the complete post-validation result: validation report, failure report, remediation plan, and approval decision.

## Basic usage

```powershell
cos-validate examples/render/lf4_engine_render_specification.yaml --evidence examples/validation/lf4_passing_evidence.yaml --artifact-id ARTIFACT-0001
```

## What it does

```text
Render Specification
  ↓
Evidence File
  ↓
Validation Approval Pipeline
  ↓
Validation Report + Failure Report + Remediation Plan + Approval Decision
```

## Evidence file format

```yaml
evidence:
  - gate_id: GATE-0001
    status: passed
    message: LF4 specificity passed.
```

## IDs

The CLI assigns default IDs, but callers can override them:

```powershell
cos-validate examples/render/lf4_engine_render_specification.yaml `
  --evidence examples/validation/lf4_passing_evidence.yaml `
  --validation-report-id VALIDATION-REPORT-0007 `
  --failure-report-id FAILURE-REPORT-0007 `
  --remediation-plan-id REMEDIATION-PLAN-0007 `
  --approval-id APPROVAL-0007
```

## Exit codes

| Exit code | Meaning |
| --- | --- |
| `0` | The approval decision is approved or approved with warnings. |
| `1` | The approval decision is rejected. |
| `2` | The CLI could not parse or evaluate the inputs. |

## Output formats

Use JSON by default:

```powershell
cos-validate examples/render/lf4_engine_render_specification.yaml --evidence examples/validation/lf4_passing_evidence.yaml
```

Use text summary output:

```powershell
cos-validate examples/render/lf4_engine_render_specification.yaml --evidence examples/validation/lf4_passing_evidence.yaml --format text
```

Write output to a file:

```powershell
cos-validate examples/render/lf4_engine_render_specification.yaml --evidence examples/validation/lf4_passing_evidence.yaml --output .constraintos/validation/lf4-result.json
```
