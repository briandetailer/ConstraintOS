# Runtime Public Evidence Package

## Purpose

This document explains the public Runtime evidence package produced by Milestone 3. It is written for external consumers that should be able to inspect Runtime evidence without importing Python internals.

The evidence package is a JSON-first boundary for audit tools, CI/CD integrations, SDKs, and future API consumers.

## Evidence package artifacts

A Runtime evidence package contains these payload artifacts:

1. Runtime report artifact.
2. Runtime trace report artifact.
3. Runtime contract registry artifact.
4. Runtime evidence manifest artifact.

The manifest links the other three artifacts and is the recommended entry point for external consumers.

## Artifact order in the evidence manifest

The manifest artifacts list must appear in this order:

```text
runtime_report
runtime_trace_report
runtime_contract_registry
```

The verifier intentionally checks this order so external tools can read predictable evidence slots.

## Manifest header

The manifest payload contains a `runtime_evidence` header:

```json
{
  "runtime_evidence": {
    "runtime_id": "RUNTIME-0001",
    "contract_registry_version": "runtime-contracts/v1",
    "runtime_report_artifact_id": "ARTIFACT-0001",
    "trace_report_artifact_id": "ARTIFACT-0002",
    "contract_registry_artifact_id": "ARTIFACT-0003",
    "artifact_count": 3
  },
  "artifacts": []
}
```

External consumers should use this header to confirm:

- which runtime produced the package
- which contract registry version applies
- which artifact id is the runtime report
- which artifact id is the trace report
- which artifact id is the contract registry report
- whether the artifact count matches the artifacts array

## Runtime report artifact

The runtime report artifact is the canonical serialized runtime result.

External consumers should use it to inspect:

- runtime id
- runtime status
- success/terminal flags
- plan payload
- schedule payload
- execution payload, when present
- runtime events
- runtime messages
- runtime summary counts

Expected artifact role:

```text
runtime_report
```

## Runtime trace report artifact

The trace report artifact is the language-neutral traceability view derived from the runtime result.

External consumers should use it to inspect:

- planned node records
- scheduled assignment records
- unscheduled node records
- execution node result records
- artifact records
- event records

Expected artifact role:

```text
runtime_trace_report
```

## Runtime contract registry artifact

The contract registry artifact declares the public Runtime contracts that external consumers can expect.

Current registry version:

```text
runtime-contracts/v1
```

Current public contracts:

- `runtime_result`
- `runtime_report`
- `runtime_traceability`
- `runtime_trace_report`
- `runtime_evidence_manifest`
- `runtime_contract_registry`

Expected artifact role:

```text
runtime_contract_registry
```

## Evidence manifest artifact metadata

The manifest artifact metadata should include:

- `artifact_role: runtime_evidence_manifest`
- `content_type: application/json`
- `runtime_id`
- `contract_registry_version`
- `runtime_report_uri`
- `trace_report_uri`
- `contract_registry_uri`

These fields allow consumers to locate the linked package artifacts without knowing internal storage rules.

## Verification rules

The Runtime evidence manifest verifier checks:

- manifest payload is readable JSON when an artifact path is supplied
- `runtime_id` is present
- `contract_registry_version` matches the current runtime contract registry version
- `artifact_count` is an integer
- `artifact_count` matches the artifacts array length
- artifacts are ordered as runtime report, trace report, then contract registry
- runtime report artifact id matches `runtime_report_artifact_id`
- trace report artifact id matches `trace_report_artifact_id`
- contract registry artifact id matches `contract_registry_artifact_id`
- runtime-bound artifacts match the manifest runtime id
- contract registry artifact has the expected registry version
- every artifact has a URI

## Consumer read sequence

External consumers should read a package in this order:

```text
1. Read evidence manifest.
2. Verify runtime_evidence header.
3. Verify artifact count and artifact roles.
4. Load runtime report URI.
5. Load trace report URI.
6. Load contract registry URI.
7. Check all artifact ids match manifest header ids.
8. Check contract registry version before interpreting contracts.
```

## Integration posture

This evidence package is the Runtime Milestone 3 handoff boundary for:

- audit tools
- CI/CD checks
- Node.js clients
- .NET clients
- Terraform/infrastructure workflows
- future hosted API consumers

Future SDKs should wrap this package shape rather than bypass it with direct Python imports.

## Milestone 3 status

This document is part of Runtime Milestone 3 external-consumer packaging. It does not add new runtime behavior.
