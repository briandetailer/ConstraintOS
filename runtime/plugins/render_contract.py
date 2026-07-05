from __future__ import annotations

from typing import Any

from runtime.context import RuntimeContext
from runtime.plugins.base import PluginResult, RuntimePlugin

REQUIRED_INPUTS_BY_ACTION = {
    "load_subject": "subject",
    "check_requirements": "requirements",
    "check_negative_constraints": "negative_constraints",
    "check_validation_gates": "gates",
}


class RenderContractPlugin(RuntimePlugin):
    """Plugin that validates render-contract runtime gate assignments."""

    name = "render_contract"
    capabilities = ["load_subject", "check_requirements", "check_negative_constraints", "check_validation_gates"]

    def execute(self, assignment: dict[str, Any], context: RuntimeContext | None = None) -> PluginResult:
        node_id = str(assignment.get("node_id", "UNKNOWN-NODE"))
        action = str(assignment.get("action", "unknown"))
        worker_id = str(assignment.get("worker_id", "PLUGIN-DISPATCHER"))
        inputs = assignment.get("inputs", {})
        if not isinstance(inputs, dict):
            raise ValueError(f"{node_id} inputs must be an object")
        required_input = REQUIRED_INPUTS_BY_ACTION.get(action)
        if required_input is None:
            raise ValueError(f"unsupported render contract action: {action}")
        if required_input not in inputs:
            raise ValueError(f"{node_id} missing required input: {required_input}")
        return PluginResult(
            plugin=self.name,
            node_id=node_id,
            action=action,
            status="complete",
            outputs=[f"render-contract://{node_id}/{action}"],
            logs=[f"Render contract gate passed: {action}."],
            metrics={"worker_id": worker_id, "required_input": required_input},
        )
