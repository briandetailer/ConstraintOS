from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from runtime.context import RuntimeContext


@dataclass(frozen=True)
class PluginResult:
    """Standard result returned by runtime plugins."""

    plugin: str
    node_id: str
    action: str
    status: str
    outputs: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    logs: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "plugin": self.plugin,
            "node_id": self.node_id,
            "action": self.action,
            "status": self.status,
            "outputs": self.outputs,
            "artifacts": self.artifacts,
            "logs": self.logs,
            "metrics": self.metrics,
        }


class RuntimePlugin(ABC):
    """Base contract for executable runtime plugins."""

    name: str
    capabilities: list[str]

    @abstractmethod
    def execute(self, assignment: dict[str, Any], context: RuntimeContext | None = None) -> PluginResult:
        """Execute a scheduled assignment and return a standardized plugin result."""
