from __future__ import annotations

import json
from pathlib import Path

from runtime.artifacts.models import RuntimeArtifact
from runtime.artifacts.store import ArtifactStore
from runtime.contracts import runtime_contract_registry, verify_runtime_contract_registry


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
