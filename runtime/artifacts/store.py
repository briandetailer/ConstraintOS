from __future__ import annotations

from pathlib import Path
from typing import Any

from runtime.artifacts.models import RuntimeArtifact


class ArtifactStoreError(ValueError):
    """Raised when an artifact store operation is invalid."""


class ArtifactStore:
    """Small local artifact ledger for runtime-produced outputs."""

    def __init__(self, root: str | Path = ".constraintos/runtime/artifacts") -> None:
        self.root = Path(root)
        self._artifacts: dict[str, RuntimeArtifact] = {}

    def register(self, artifact: RuntimeArtifact) -> RuntimeArtifact:
        if not artifact.id:
            raise ArtifactStoreError("artifact id is required")
        if not artifact.uri:
            raise ArtifactStoreError("artifact uri is required")
        if artifact.id in self._artifacts:
            raise ArtifactStoreError(f"Artifact {artifact.id} is already registered")
        self._artifacts[artifact.id] = artifact
        return artifact

    def record_uri(
        self,
        uri: str,
        artifact_id: str | None = None,
        kind: str = "file",
        producer: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> RuntimeArtifact:
        artifact = RuntimeArtifact(
            id=artifact_id or self._next_artifact_id(),
            uri=uri,
            kind=kind,
            producer=producer,
            metadata=metadata or {},
        )
        return self.register(artifact)

    def write_text(
        self,
        relative_path: str | Path,
        content: str,
        artifact_id: str | None = None,
        producer: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> RuntimeArtifact:
        path = self._resolve_relative_path(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return self.record_uri(
            uri=path.as_uri(),
            artifact_id=artifact_id,
            kind="file",
            producer=producer,
            metadata={"path": str(path), **(metadata or {})},
        )

    def get(self, artifact_id: str) -> RuntimeArtifact:
        try:
            return self._artifacts[artifact_id]
        except KeyError as error:
            raise ArtifactStoreError(f"Artifact {artifact_id} is not registered") from error

    def list(self) -> list[RuntimeArtifact]:
        return list(self._artifacts.values())

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_store": {
                "root": str(self.root),
                "count": len(self._artifacts),
            },
            "artifacts": [artifact.to_dict() for artifact in self.list()],
        }

    def _next_artifact_id(self) -> str:
        return f"ARTIFACT-{len(self._artifacts) + 1:04d}"

    def _resolve_relative_path(self, relative_path: str | Path) -> Path:
        path = Path(relative_path)
        if path.is_absolute():
            raise ArtifactStoreError("artifact path must be relative to the artifact store root")
        if any(part == ".." for part in path.parts):
            raise ArtifactStoreError("artifact path cannot escape the artifact store root")
        return (self.root / path).resolve()
