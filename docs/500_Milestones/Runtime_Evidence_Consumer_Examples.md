# Runtime Evidence Consumer Examples

## Purpose

This document shows how external consumers can read a Runtime evidence package without importing Python Runtime internals.

The examples are intentionally lightweight. They model the evidence package contract from the consumer's point of view and should later become SDK examples for Node.js, .NET, CI/CD, and hosted API integrations.

## Evidence package entry point

External consumers should start from the evidence manifest JSON.

The manifest links:

- runtime report artifact
- runtime trace report artifact
- runtime contract registry artifact

The expected artifact role order is:

```text
runtime_report
runtime_trace_report
runtime_contract_registry
```

## Shared validation checklist

A consumer should verify the manifest before trusting the package:

1. `runtime_evidence` exists.
2. `runtime_id` is present.
3. `contract_registry_version` is present.
4. `artifact_count` equals `artifacts.length`.
5. Artifact roles appear in the expected order.
6. Header artifact ids match artifact ids in the artifacts array.
7. Every artifact has a URI.
8. The contract registry artifact has the expected registry version.

## Node.js / TypeScript-style example

```ts
import { readFile } from "node:fs/promises";

type EvidenceArtifact = {
  id: string;
  uri: string;
  metadata?: Record<string, unknown>;
};

type EvidenceManifest = {
  runtime_evidence: {
    runtime_id: string;
    contract_registry_version: string;
    runtime_report_artifact_id: string;
    trace_report_artifact_id: string;
    contract_registry_artifact_id: string;
    artifact_count: number;
  };
  artifacts: EvidenceArtifact[];
};

const EXPECTED_ROLES = [
  "runtime_report",
  "runtime_trace_report",
  "runtime_contract_registry",
];

export async function readEvidenceManifest(path: string): Promise<EvidenceManifest> {
  const raw = await readFile(path, "utf8");
  return JSON.parse(raw) as EvidenceManifest;
}

export function verifyEvidenceManifest(manifest: EvidenceManifest): string[] {
  const issues: string[] = [];
  const evidence = manifest.runtime_evidence;
  const artifacts = manifest.artifacts ?? [];

  if (!evidence?.runtime_id) {
    issues.push("runtime_id is required");
  }
  if (!evidence?.contract_registry_version) {
    issues.push("contract_registry_version is required");
  }
  if (evidence?.artifact_count !== artifacts.length) {
    issues.push("artifact_count must match artifacts length");
  }

  const roles = artifacts.map((artifact) => artifact.metadata?.artifact_role);
  if (JSON.stringify(roles) !== JSON.stringify(EXPECTED_ROLES)) {
    issues.push("artifacts must be runtime_report, runtime_trace_report, runtime_contract_registry");
  }

  if (artifacts[0]?.id !== evidence?.runtime_report_artifact_id) {
    issues.push("runtime_report_artifact_id must match runtime report artifact id");
  }
  if (artifacts[1]?.id !== evidence?.trace_report_artifact_id) {
    issues.push("trace_report_artifact_id must match trace report artifact id");
  }
  if (artifacts[2]?.id !== evidence?.contract_registry_artifact_id) {
    issues.push("contract_registry_artifact_id must match contract registry artifact id");
  }

  artifacts.forEach((artifact, index) => {
    if (!artifact.uri) {
      issues.push(`artifact ${index + 1} requires uri`);
    }
  });

  if (artifacts[2]?.metadata?.registry_version !== evidence?.contract_registry_version) {
    issues.push("contract registry artifact version must match evidence contract_registry_version");
  }

  return issues;
}
```

## C# / .NET-style example

```csharp
using System.Text.Json;

public sealed record EvidenceManifest(
    RuntimeEvidence runtime_evidence,
    EvidenceArtifact[] artifacts
);

public sealed record RuntimeEvidence(
    string runtime_id,
    string contract_registry_version,
    string runtime_report_artifact_id,
    string trace_report_artifact_id,
    string contract_registry_artifact_id,
    int artifact_count
);

public sealed record EvidenceArtifact(
    string id,
    string uri,
    Dictionary<string, JsonElement>? metadata
);

public static class RuntimeEvidenceVerifier
{
    private static readonly string[] ExpectedRoles =
    {
        "runtime_report",
        "runtime_trace_report",
        "runtime_contract_registry",
    };

    public static async Task<EvidenceManifest> ReadEvidenceManifestAsync(string path)
    {
        await using var stream = File.OpenRead(path);
        var manifest = await JsonSerializer.DeserializeAsync<EvidenceManifest>(stream);
        return manifest ?? throw new InvalidOperationException("Evidence manifest could not be parsed.");
    }

    public static IReadOnlyList<string> VerifyEvidenceManifest(EvidenceManifest manifest)
    {
        var issues = new List<string>();
        var evidence = manifest.runtime_evidence;
        var artifacts = manifest.artifacts ?? Array.Empty<EvidenceArtifact>();

        if (string.IsNullOrWhiteSpace(evidence.runtime_id))
        {
            issues.Add("runtime_id is required");
        }

        if (string.IsNullOrWhiteSpace(evidence.contract_registry_version))
        {
            issues.Add("contract_registry_version is required");
        }

        if (evidence.artifact_count != artifacts.Length)
        {
            issues.Add("artifact_count must match artifacts length");
        }

        var roles = artifacts
            .Select(artifact => MetadataString(artifact, "artifact_role"))
            .ToArray();

        if (!roles.SequenceEqual(ExpectedRoles))
        {
            issues.Add("artifacts must be runtime_report, runtime_trace_report, runtime_contract_registry");
        }

        if (artifacts.ElementAtOrDefault(0)?.id != evidence.runtime_report_artifact_id)
        {
            issues.Add("runtime_report_artifact_id must match runtime report artifact id");
        }

        if (artifacts.ElementAtOrDefault(1)?.id != evidence.trace_report_artifact_id)
        {
            issues.Add("trace_report_artifact_id must match trace report artifact id");
        }

        if (artifacts.ElementAtOrDefault(2)?.id != evidence.contract_registry_artifact_id)
        {
            issues.Add("contract_registry_artifact_id must match contract registry artifact id");
        }

        for (var index = 0; index < artifacts.Length; index++)
        {
            if (string.IsNullOrWhiteSpace(artifacts[index].uri))
            {
                issues.Add($"artifact {index + 1} requires uri");
            }
        }

        var registryVersion = artifacts.ElementAtOrDefault(2) is { } registry
            ? MetadataString(registry, "registry_version")
            : null;

        if (registryVersion != evidence.contract_registry_version)
        {
            issues.Add("contract registry artifact version must match evidence contract_registry_version");
        }

        return issues;
    }

    private static string? MetadataString(EvidenceArtifact artifact, string key)
    {
        if (artifact.metadata is null || !artifact.metadata.TryGetValue(key, out var value))
        {
            return null;
        }

        return value.ValueKind == JsonValueKind.String ? value.GetString() : null;
    }
}
```

## CI/CD usage pattern

A CI/CD integration should treat the manifest as a gate:

```text
1. Generate or receive Runtime evidence package.
2. Read evidence manifest.
3. Verify manifest structure and linked artifact roles.
4. Verify contract registry version.
5. Load runtime report and inspect runtime_result.status.
6. Load trace report and inspect trace record coverage.
7. Fail the build if manifest verification fails or runtime status is unacceptable.
```

## SDK direction

Future SDKs should hide the file-loading details but preserve the same contract checks.

A future SDK should expose something like:

```text
EvidencePackage.Load(path)
EvidencePackage.Verify()
EvidencePackage.RuntimeReport
EvidencePackage.TraceReport
EvidencePackage.ContractRegistry
```

SDKs should not bypass the evidence manifest or depend on Python object models.
