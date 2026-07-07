# Runtime JSON Schema Target

## Purpose

This document defines the Milestone 3 target for promoting Runtime contract inventory into formal JSON Schema files.

Milestone 3 established public Runtime contracts, verifiers, reports, traceability artifacts, evidence bundles, CLI generation, and external-consumer packaging guidance. The schema work turns those documented and verified shapes into schema files that non-Python consumers can validate directly.

## Status

Current status:

```text
implemented / current public Runtime schema set complete
```

Runtime contracts are currently represented by:

- Python dataclasses and serializers
- public contract registry entries
- verifier functions
- JSON Schema files
- tests
- documentation
- example consumer guidance

The current public evidence-boundary schema set is implemented and test-backed.

## Schema goals

JSON Schema provides:

- language-neutral validation
- stable external contract references
- CI/CD validation support
- SDK generation inputs
- audit-tool compatibility
- explicit contract versioning

The schema files do not replace the Python verifiers. They complement them so external consumers can validate payloads without importing Python Runtime internals.

## Schema location

```text
schemas/runtime/v1/
  runtime-result.schema.json
  runtime-report.schema.json
  runtime-traceability.schema.json
  runtime-trace-report.schema.json
  runtime-evidence-manifest.schema.json
  runtime-contract-registry.schema.json
```

## Implemented schema set

### runtime-result.schema.json

Status:

```text
implemented
```

Validates the canonical serialized runtime result payload.

Covers:

- `runtime_result` header shape
- runtime id
- runtime status enum
- success, terminal, and successful flags
- created date string
- summary count shape
- event envelope shape
- runtime event type enum
- messages array
- flexible nested `plan`, `schedule`, `execution`, and `artifacts` objects

### runtime-report.schema.json

Status:

```text
implemented
```

Validates persisted runtime report artifact wrappers.

Covers:

- artifact id
- artifact URI
- file kind
- producer runtime id
- artifact metadata shape
- `artifact_role: runtime_report`
- `content_type: application/json`
- runtime id
- runtime status enum
- runtime success flag
- summary object
- artifact path

The runtime report payload itself is validated by `runtime-result.schema.json`.

### runtime-traceability.schema.json

Status:

```text
implemented
```

Validates the traceability payload generated from a runtime result.

Covers:

- `runtime_traceability` header shape
- runtime id
- runtime status string
- success flag
- record count shape
- trace records array
- trace record ids
- trace record type enum
- source ids
- runtime ids
- record status strings
- nullable or string parent ids
- metadata object shape

### runtime-trace-report.schema.json

Status:

```text
implemented
```

Validates persisted runtime trace report artifact wrappers.

Covers:

- artifact id
- artifact URI
- file kind
- producer runtime id
- artifact metadata shape
- `artifact_role: runtime_trace_report`
- `content_type: application/json`
- runtime id
- trace status string
- trace success flag
- record count shape
- artifact path

The trace report payload itself is validated by `runtime-traceability.schema.json`.

### runtime-evidence-manifest.schema.json

Status:

```text
implemented
```

Validates the public evidence package manifest.

Covers:

- `runtime_evidence` header shape
- runtime id
- contract registry version
- runtime report artifact id
- trace report artifact id
- contract registry artifact id
- artifact count
- exactly three artifacts
- artifact role order through positional artifact definitions
- runtime report artifact wrapper shape
- trace report artifact wrapper shape
- contract registry artifact wrapper shape
- URI presence

Note: JSON Schema validates structure, required fields, roles, constants, and artifact order. Cross-field checks, such as exact id matching between header fields and artifact entries, remain in the Python evidence manifest verifier.

### runtime-contract-registry.schema.json

Status:

```text
implemented
```

Validates the Runtime contract registry artifact.

Covers:

- registry version
- contract count shape
- contract list shape
- required contract fields
- `produced_by`
- `consumed_by`
- required sections
- supported contract types
- rejection of unknown contract fields

## Contract registry linkage

The Runtime contract registry should eventually include schema references.

Example future contract entry field:

```json
{
  "name": "runtime_evidence_manifest",
  "version": "v1",
  "contract_type": "artifact_json",
  "schema": "schemas/runtime/v1/runtime-evidence-manifest.schema.json"
}
```

This should be added carefully because it changes the public contract registry shape.

## Verification strategy

The JSON Schema promotion is test-backed.

Current implemented checks:

1. Current contract registry passes `runtime-contract-registry.schema.json`.
2. Missing required contract fields fail schema validation.
3. Unknown contract types fail schema validation.
4. Current generated runtime result passes `runtime-result.schema.json`.
5. Unknown runtime result status fails schema validation.
6. Negative runtime result summary counts fail schema validation.
7. Current traceability payload passes `runtime-traceability.schema.json`.
8. Unknown trace record type fails schema validation.
9. Non-object trace record metadata fails schema validation.
10. Current runtime report artifact passes `runtime-report.schema.json`.
11. Wrong runtime report artifact role fails schema validation.
12. Missing runtime report runtime id fails schema validation.
13. Current trace report artifact passes `runtime-trace-report.schema.json`.
14. Wrong trace report artifact role fails schema validation.
15. Negative trace report record count fails schema validation.
16. Current evidence manifest passes `runtime-evidence-manifest.schema.json`.
17. Wrong evidence manifest artifact order fails schema validation.
18. Wrong evidence manifest registry version fails schema validation.
19. Wrong evidence manifest artifact count fails schema validation.

Future checks may add stronger cross-field agreement tests between schema validation and Python verifiers where JSON Schema can express the same constraints.

## External-consumer value

External consumers can validate Runtime evidence packages using standard JSON Schema tooling in:

- Node.js
- .NET
- Java
- Python
- Terraform-adjacent workflows
- CI/CD systems
- audit pipelines

## Milestone 3 disposition

This target is complete for the current Runtime Milestone 3 public evidence-boundary schema set.

All six planned schemas are implemented and test-backed: `runtime-contract-registry.schema.json`, `runtime-result.schema.json`, `runtime-traceability.schema.json`, `runtime-report.schema.json`, `runtime-trace-report.schema.json`, and `runtime-evidence-manifest.schema.json`.
