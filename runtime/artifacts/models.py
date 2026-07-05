from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RuntimeArtifact:
    """Metadata record for an artifact produced or consumed by runtime execution."""

    id: str
    uri: str
    kind: str = "file"
    producer: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "uri": self.uri,
            "kind": self.kind,
            "producer": self.producer,
            "metadata": self.metadata,
        }
