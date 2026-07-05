from __future__ import annotations

from typing import Any

from runtime.context import RuntimeContext
from runtime.plugins.base import PluginResult, RuntimePlugin


class DryRunPlugin(RuntimePlugin):
    """Plugin that simulates assignment execution without side effects."""

    name = "dry_run"
    capabilities = ["simulate"]

    def execute(self, assignment: dict[str, Any], context: RuntimeContext | None = None) -> PluginResult:
        node_id = str(assignment.get("node_id", "UNKNOWN-NODE"))
        action = str(assignment.get("action", "unknown"))
        return PluginResult(
            plugin=self.name,
            node_id=node_id,
            action=action,
            status="dry_run_complete",
            outputs=[f"dry-run://{node_id}"],
            logs=["Assignment simulated successfully."],
            metrics={"side_effects": 0},
        )
