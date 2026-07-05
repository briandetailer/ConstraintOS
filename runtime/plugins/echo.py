from __future__ import annotations

from typing import Any

from runtime.context import RuntimeContext
from runtime.plugins.base import PluginResult, RuntimePlugin


class EchoPlugin(RuntimePlugin):
    """Plugin that echoes assignment details for deterministic integration tests."""

    name = "echo"
    capabilities = ["echo"]

    def execute(self, assignment: dict[str, Any], context: RuntimeContext | None = None) -> PluginResult:
        node_id = str(assignment.get("node_id", "UNKNOWN-NODE"))
        action = str(assignment.get("action", "unknown"))
        worker_id = str(assignment.get("worker_id", "PLUGIN-DISPATCHER"))
        return PluginResult(
            plugin=self.name,
            node_id=node_id,
            action=action,
            status="complete",
            outputs=[f"echo://{node_id}"],
            logs=[f"Executed {action} for {node_id}."],
            metrics={"worker_id": worker_id},
        )
