from __future__ import annotations

from typing import Any

from runtime.context import RuntimeContext
from runtime.execution.executor import ExecutionError
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
            raise ExecutionError("assignments must be a list")

        node_results = [self._execute_assignment(assignment, context) for assignment in assignments if isinstance(assignment, dict)]
        status = "complete" if len(node_results) == len(assignments) and all(self._node_successful(result) for result in node_results) else "partial"
        return ExecutionResult(
            id=result_id,
            request_id=request_id,
            status=status,
            node_results=node_results,
            messages=["Plugin execution completed." if status == "complete" else "Plugin execution completed with failed or skipped assignments."],
        )

    def _execute_assignment(self, assignment: dict[str, Any], context: RuntimeContext | None = None) -> NodeExecutionResult:
        try:
            plugin_result = self.dispatcher.dispatch(assignment, context)
            return self._node_result_from_plugin_result(plugin_result)
        except Exception as error:
            return self._failed_node_result(assignment, error)

    def _node_result_from_plugin_result(self, result: PluginResult) -> NodeExecutionResult:
        self._validate_plugin_result(result)
        return NodeExecutionResult(
            node_id=result.node_id,
            worker_id=result.metrics.get("worker_id", "PLUGIN-DISPATCHER"),
            plugin=result.plugin,
            action=result.action,
            status=result.status,
            outputs=result.outputs,
            message="\n".join(result.logs),
        )

    def _validate_plugin_result(self, result: Any) -> None:
        if not isinstance(result, PluginResult):
            raise ExecutionError("plugin dispatcher must return PluginResult")
        for field_name in ("plugin", "node_id", "action", "status"):
            if not isinstance(getattr(result, field_name), str) or not getattr(result, field_name):
                raise ExecutionError(f"plugin result {field_name} must be a non-empty string")
        if not isinstance(result.outputs, list) or not all(isinstance(output, str) for output in result.outputs):
            raise ExecutionError("plugin result outputs must be a list of strings")
        if not isinstance(result.logs, list) or not all(isinstance(log, str) for log in result.logs):
            raise ExecutionError("plugin result logs must be a list of strings")
        if not isinstance(result.metrics, dict):
            raise ExecutionError("plugin result metrics must be a dictionary")

    def _failed_node_result(self, assignment: dict[str, Any], error: Exception) -> NodeExecutionResult:
        return NodeExecutionResult(
            node_id=str(assignment.get("node_id", "UNKNOWN-NODE")),
            worker_id=str(assignment.get("worker_id", "UNKNOWN-WORKER")),
            plugin=str(assignment.get("plugin", "unknown")),
            action=str(assignment.get("action", "unknown")),
            status="plugin_execution_failed",
            outputs=[],
            message=str(error),
        )

    def _node_successful(self, result: NodeExecutionResult) -> bool:
        return result.status not in {"failed", "plugin_execution_failed", "plugin_result_invalid"}
