# Runtime JSON Schema Target

## Purpose

This document defines the post-Milestone 3 target for promoting Runtime contract inventory into formal JSON Schema files.

Milestone 3 established public Runtime contracts, verifiers, reports, traceability artifacts, evidence bundles, and external-consumer packaging guidance. The next packaging/integration milestone should turn those documented and verified shapes into schema files that non-Python consumers can validate directly.

## Status

Current status:

```text
target defined / schema files not yet implemented
```

Runtime contracts are currently represented by:

- Python dataclasses and serializers
- public contract registry entries
- verifier functions
- tests
- documentation
- example consumer guidance

The next step is to publish language-neutral JSON Schema files for the public evidence boundary.

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

Validates the canonical serialized runtime result payload.

Should cover:

- `runtime_result`
- `summary`
- `plan`
- `schedule`
- `execution`, when present
- `events`
- `messages`
- `artifacts`, when present

### runtime-report.schema.json

Validates persisted runtime report artifacts.

Should cover:

- artifact wrapper shape
- artifact metadata
- embedded or linked runtime result payload
- `artifact_role: runtime_report`
- `content_type: application/json`

### runtime-traceability.schema.json

Validates the traceability payload generated from a runtime result.

Should cover:

- `runtime_traceability`
- trace records
- record ids
- record types
- runtime id alignment
- metadata shape

### runtime-trace-report.schema.json

Validates persisted trace report artifacts.

Should cover:

- artifact wrapper shape
- trace payload
- trace metadata
- `artifact_role: runtime_trace_report`
- `content_type: application/json`

### runtime-evidence-manifest.schema.json

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

Validates the Runtime contract registry artifact.

Should cover:

- registry version
- contract count
- contract list
- required contract fields
- `produced_by`
- `consumed_by`
- required sections
- contract type

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

Tests should verify:

1. Current generated runtime result passes `runtime-result.schema.json`.
2. Current runtime report artifact passes `runtime-report.schema.json`.
3. Current traceability payload passes `runtime-traceability.schema.json`.
4. Current trace report artifact passes `runtime-trace-report.schema.json`.
5. Current evidence manifest passes `runtime-evidence-manifest.schema.json`.
6. Current contract registry passes `runtime-contract-registry.schema.json`.
7. Known malformed payloads fail the expected schema checks.
8. Python verifiers and JSON Schema validation agree on supported payload classes.

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

This target does not block Runtime Milestone 3 closeout.

It should be treated as a packaging/integration follow-up after Milestone 3 closes.
