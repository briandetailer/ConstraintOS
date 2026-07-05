from __future__ import annotations

from typing import Any

from runtime.context import RuntimeContext
from runtime.execution.models import ExecutionRequest, ExecutionResult, NodeExecutionResult
from runtime.plugins import PluginDispatcher, PluginResult


class PluginExecutor:
    """Executes assignments by dispatching them to registered runtime plugins."""

    def __init__(self, dispatcher: PluginDispatcher) -> None:
        self.dispatcher = dispatcher

    def execute(
        self,
        request: ExecutionRequest | dict[str, Any],
        result_id: str = "EXEC-RESULT-0001",
        context: RuntimeContext | None = None,
    ) -> ExecutionResult:
        request_data = request.to_dict() if isinstance(request, ExecutionRequest) else request
        request_meta = request_data.get("execution_request", {})
        request_id = str(request_meta.get("id", "UNKNOWN-REQUEST"))
        assignments = request_data.get("assignments", [])
        if not isinstance(assignments, list):
            raise ValueError("assignments must be a list")

        plugin_results = [self.dispatcher.dispatch(assignment, context) for assignment in assignments if isinstance(assignment, dict)]
        node_results = [self._node_result_from_plugin_result(result) for result in plugin_results]
        status = "complete" if len(node_results) == len(assignments) else "partial"
        return ExecutionResult(
            id=result_id,
            request_id=request_id,
            status=status,
            node_results=node_results,
            messages=["Plugin execution completed." if status == "complete" else "Plugin execution completed with skipped assignments."],
        )

    def _node_result_from_plugin_result(self, result: PluginResult) -> NodeExecutionResult:
        return NodeExecutionResult(
            node_id=result.node_id,
            worker_id=result.metrics.get("worker_id", "PLUGIN-DISPATCHER"),
            plugin=result.plugin,
            action=result.action,
            status=result.status,
            outputs=result.outputs,
            message="\n".join(result.logs),
        )
