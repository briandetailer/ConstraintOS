# Runtime JSON Schema Target

## Purpose

This document defines the Milestone 3 target for promoting Runtime contract inventory into formal JSON Schema files.

Milestone 3 established public Runtime contracts, verifiers, reports, traceability artifacts, evidence bundles, CLI generation, and external-consumer packaging guidance. The schema work turns those documented and verified shapes into schema files that non-Python consumers can validate directly.

## Status

Current status:

```text
in progress / runtime result and contract registry schemas implemented
```

Runtime contracts are currently represented by:

- Python dataclasses and serializers
- public contract registry entries
- verifier functions
- JSON Schema files
- tests
- documentation
- example consumer guidance

The next step is to continue publishing language-neutral JSON Schema files for the public evidence boundary.

## Schema goals

JSON Schema should provide:

- language-neutral validation
- stable external contract references
- CI/CD validation support
- SDK generation inputs
- audit-tool compatibility
- explicit contract versioning

The schema files should not replace the Python verifiers. They should complement them so external consumers can validate payloads without importing Python Runtime internals.

## Proposed schema location

```text
schemas/runtime/v1/
  runtime-result.schema.json
  runtime-report.schema.json
  runtime-traceability.schema.json
  runtime-trace-report.schema.json
  runtime-evidence-manifest.schema.json
  runtime-contract-registry.schema.json
```

## Initial schema set

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
not implemented
```

Validates persisted runtime report artifacts.

Should cover:

- artifact wrapper shape
- artifact metadata
- embedded or linked runtime result payload
- `artifact_role: runtime_report`
- `content_type: application/json`

### runtime-traceability.schema.json

Status:

```text
not implemented
```

Validates the traceability payload generated from a runtime result.

Should cover:

- `runtime_traceability`
- trace records
- record ids
- record types
- runtime id alignment
- metadata shape

### runtime-trace-report.schema.json

Status:

```text
not implemented
```

Validates persisted trace report artifacts.

Should cover:

- artifact wrapper shape
- trace payload
- trace metadata
- `artifact_role: runtime_trace_report`
- `content_type: application/json`

### runtime-evidence-manifest.schema.json

Status:

```text
not implemented
```

Validates the public evidence package manifest.

Should cover:

- `runtime_evidence`
- runtime id
- contract registry version
- runtime report artifact id
- trace report artifact id
- contract registry artifact id
- artifact count
- artifacts list
- artifact role order, where possible
- URI presence

Note: JSON Schema can validate structure, required fields, and enums. Some cross-field checks, such as exact id matching between header fields and artifact entries, may still require verifier logic.

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

The JSON Schema promotion should be test-backed.

Current implemented checks:

1. Current contract registry passes `runtime-contract-registry.schema.json`.
2. Missing required contract fields fail schema validation.
3. Unknown contract types fail schema validation.
4. Current generated runtime result passes `runtime-result.schema.json`.
5. Unknown runtime result status fails schema validation.
6. Negative runtime result summary counts fail schema validation.

Remaining checks should verify:

1. Current runtime report artifact passes `runtime-report.schema.json`.
2. Current traceability payload passes `runtime-traceability.schema.json`.
3. Current trace report artifact passes `runtime-trace-report.schema.json`.
4. Current evidence manifest passes `runtime-evidence-manifest.schema.json`.
5. Known malformed payloads fail the expected schema checks.
6. Python verifiers and JSON Schema validation agree on supported payload classes where the checks overlap.

## External-consumer value

Once implemented, external consumers can validate Runtime evidence packages using standard JSON Schema tooling in:

- Node.js
- .NET
- Java
- Python
- Terraform-adjacent workflows
- CI/CD systems
- audit pipelines

## Milestone 3 disposition

This target is now active Runtime Milestone 3 implementation work.

The first two schemas, `runtime-contract-registry.schema.json` and `runtime-result.schema.json`, are implemented and test-backed. The remaining schemas should continue in small, green slices.
