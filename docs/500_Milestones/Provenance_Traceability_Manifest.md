# Provenance Manifest / Traceability Manifest

## Status

Implemented.

## Scope

This milestone adds a deterministic provenance manifest to validation approval results. The manifest is intended to be the root-level audit surface for the validation approval pipeline while preserving existing nested reports.

## Guarantees

- A provenance manifest schema exists and is registered.
- Validation approval results include a root-level `provenance_manifest`.
- The manifest records the validation report, failure report, remediation plan, revision request, and approval decision as traceability nodes.
- The manifest records gate-level traceability for every validation result.
- Gate traceability includes gate id, gate name, status, required/optional policy, evidence status, and issue code.
- The manifest copies the root constraint pack audit header from the validation report.
- The manifest status follows the approval decision status.
- The `cos-validate` JSON output includes the manifest.
- The `cos-validate --format text` summary reports the manifest id, status, and gate count.
- The manifest can be validated through the normal schema registry path.

## Contract Shape

```yaml
provenance_manifest:
  id: PROVENANCE-0001
  created: "YYYY-MM-DD"
  status: approved
  source: validation_approval_pipeline
  constraint_packs: []
subject:
  id: SUBJECT-0001
artifact:
  id: ARTIFACT-0001
validation:
  report_id: VALIDATION-REPORT-0001
  status: passed
  result_count: 3
traceability:
  nodes: []
  gates: []
```

## Rationale

The validation approval pipeline already produces nested artifacts for validation, failure analysis, remediation, revision, and approval. The provenance manifest gives downstream callers a single deterministic traceability surface without removing or weakening those nested artifacts.
