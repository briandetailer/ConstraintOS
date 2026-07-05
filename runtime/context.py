from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RuntimeContext:
    """Immutable context passed through runtime orchestration."""

    workspace: Path = Path(".")
    variables: dict[str, Any] = field(default_factory=dict)
    artifacts: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "workspace": str(self.workspace),
            "variables": self.variables,
            "artifacts": self.artifacts,
        }
