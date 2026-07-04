from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Protocol


@dataclass
class StoredObject:
    id: str
    uri: str
    media_type: str
    size_bytes: int
    created: str

    def to_dict(self) -> dict:
        return {
            "stored_object": {
                "id": self.id,
                "uri": self.uri,
                "media_type": self.media_type,
                "size_bytes": self.size_bytes,
                "created": self.created,
            }
        }


class StorageBackend(Protocol):
    """Storage backend protocol for artifact outputs."""

    def put_text(self, object_id: str, content: str, media_type: str = "text/plain") -> StoredObject:
        """Persist text and return a storage object reference."""

    def get_text(self, object_id: str) -> str:
        """Read stored text by object ID."""


class LocalStorageBackend:
    """Local filesystem-backed storage adapter."""

    def __init__(self, root: str | Path = "artifact_store") -> None:
        self.root = Path(root)

    def _path_for(self, object_id: str) -> Path:
        safe_id = object_id.replace("/", "_").replace("..", "_")
        return self.root / safe_id

    def put_text(self, object_id: str, content: str, media_type: str = "text/plain") -> StoredObject:
        path = self._path_for(object_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return StoredObject(
            id=object_id,
            uri=f"file://{path.as_posix()}",
            media_type=media_type,
            size_bytes=len(content.encode("utf-8")),
            created=date.today().isoformat(),
        )

    def get_text(self, object_id: str) -> str:
        return self._path_for(object_id).read_text(encoding="utf-8")


def create_artifact_repository_layout(root: str | Path = "artifact_store") -> dict:
    base = Path(root)
    paths = {
        "root": base,
        "outputs": base / "outputs",
        "manifests": base / "manifests",
        "reports": base / "reports",
        "patches": base / "patches",
        "baselines": base / "baselines",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return {key: str(value) for key, value in paths.items()}
