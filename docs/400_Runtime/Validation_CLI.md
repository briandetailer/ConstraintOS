# Validation CLI

`cos-validate` runs the validation approval pipeline from the command line.

It evaluates a render specification against supplied validation evidence, then produces the complete post-validation result: validation report, failure report, remediation plan, revision request, and approval decision.

## Basic usage

```powershell
cos-validate examples/render/lf4_engine_render_specification.yaml --evidence examples/validation/lf4_passing_evidence.yaml --artifact-id ARTIFACT-0001
```

## What it does

```text
Render Specification
  ↓
Optional Constraint Packs
  ↓
Evidence File
  ↓
Validation Approval Pipeline
  ↓
Validation Report + Failure Report + Remediation Plan + Revision Request + Approval Decision
```

## Evidence file format

```yaml
evidence:
  - gate_id: GATE-0001
    status: passed
    message: LF4 specificity passed.
```

Evidence files are validated against the registered Validation Evidence schema before the validation pipeline runs.

## Constraint packs

Constraint packs can be applied before validation:

```powershell
cos-validate examples/render/lf4_engine_render_specification.yaml `
  --constraint-pack examples/constraint_packs/lf4_engine_constraint_pack.yaml `
  --evidence examples/validation/lf4_passing_evidence.yaml
```

Use `--constraint-pack` more than once to apply multiple packs in order.

Applied pack references are preserved in the JSON output under each generated report/decision header, including validation, failure report, remediation plan, revision request, and approval decision.

Text summary output includes the applied constraint pack count.

## Schema validation

`cos-validate` validates the render specification, every supplied constraint pack, and the evidence file against their registered schemas before validation begins.

Malformed render specifications, constraint packs, or evidence files return exit code `2` with a schema error that names the schema path and failing field.

## IDs

The CLI assigns default IDs, but callers can override them:

```powershell
cos-validate examples/render/lf4_engine_render_specification.yaml `
  --evidence examples/validation/lf4_passing_evidence.yaml `
  --validation-report-id VALIDATION-REPORT-0007 `
  --failure-report-id FAILURE-REPORT-0007 `
  --remediation-plan-id REMEDIATION-PLAN-0007 `
  --revision-request-id REVISION-REQUEST-0007 `
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
