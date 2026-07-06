from __future__ import annotations

import json
from pathlib import Path

from runtime.artifacts.models import RuntimeArtifact
from runtime.artifacts.store import ArtifactStore
from runtime.contracts import RuntimeContractVerification, runtime_contract_registry, verify_runtime_contract_registry


class RuntimeContractRegistryReportWriter:
    """Writes the runtime contract registry as a JSON artifact."""

    def __init__(self, store: ArtifactStore | None = None) -> None:
        self.store = store or ArtifactStore()

    def write_registry(self, relative_path: str | Path | None = None) -> RuntimeArtifact:
        registry = runtime_contract_registry()
        verification = verify_runtime_contract_registry(registry)
        if not verification.successful():
            raise ValueError("Runtime contract registry report requires a valid registry.")

        header = registry["runtime_contract_registry"]
        registry_path = relative_path or "contracts/runtime-contract-registry.json"
        content = json.dumps(registry, indent=2, sort_keys=True) + "\n"
        return self.store.write_text(
            registry_path,
            content,
            producer=str(header["version"]),
            metadata={
                "artifact_role": "runtime_contract_registry",
                "content_type": "application/json",
                "registry_version": header["version"],
                "contract_count": header["contract_count"],
            },
        )


def verify_runtime_contract_registry_report(artifact: RuntimeArtifact | dict[str, object]) -> RuntimeContractVerification:
    artifact_data = artifact.to_dict() if isinstance(artifact, RuntimeArtifact) else artifact
    if not isinstance(artifact_data, dict):
        return RuntimeContractVerification(["Runtime contract registry report must be a dictionary or RuntimeArtifact."])

    metadata = artifact_data.get("metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}
    path = metadata.get("path")
    if not isinstance(path, str) or not path:
        return RuntimeContractVerification(["Runtime contract registry report artifact path is required."])

    try:
        registry = json.loads(Path(path).read_text(encoding="utf-8"))
    except OSError:
        return RuntimeContractVerification(["Runtime contract registry report artifact path must be readable."])
    except json.JSONDecodeError:
        return RuntimeContractVerification(["Runtime contract registry report artifact content must be valid JSON."])

    verification = verify_runtime_contract_registry(registry)
    issues = list(verification.issues)
    header = registry.get("runtime_contract_registry", {}) if isinstance(registry, dict) else {}
    if not isinstance(header, dict):
        header = {}
    if metadata.get("artifact_role") != "runtime_contract_registry":
        issues.append("Runtime contract registry report artifact_role must be runtime_contract_registry.")
    if metadata.get("content_type") != "application/json":
        issues.append("Runtime contract registry report content_type must be application/json.")
    if metadata.get("registry_version") != header.get("version"):
        issues.append("Runtime contract registry report registry_version must match registry version.")
    if metadata.get("contract_count") != header.get("contract_count"):
        issues.append("Runtime contract registry report contract_count must match registry contract_count.")

    return RuntimeContractVerification(issues)
