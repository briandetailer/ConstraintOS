from __future__ import annotations

from typing import Any

from runtime.execution.models import ExecutionRequest, ExecutionResult, NodeExecutionResult


class ExecutionError(ValueError):
    """Raised when an execution request is invalid."""


class DryRunExecutor:
    def execute(self, request: ExecutionRequest | dict[str, Any], result_id: str = "EXEC-RESULT-0001") -> ExecutionResult:
        request_data = request.to_dict() if isinstance(request, ExecutionRequest) else request
        request_meta = request_data.get("execution_request", {})
        request_id = str(request_meta.get("id", "UNKNOWN-REQUEST"))
        dry_run = bool(request_meta.get("dry_run", True))
        if not dry_run:
            raise ExecutionError("DryRunExecutor only accepts dry-run requests")
        assignments = request_data.get("assignments", [])
        if not isinstance(assignments, list):
            raise ExecutionError("assignments must be a list")
        node_results = [self._execute_assignment(assignment) for assignment in assignments if isinstance(assignment, dict)]
        status = "complete" if len(node_results) == len(assignments) else "partial"
        return ExecutionResult(
            id=result_id,
            request_id=request_id,
            status=status,
            node_results=node_results,
            messages=["Dry-run execution completed." if status == "complete" else "Dry-run execution completed with skipped assignments."],
        )

    def _execute_assignment(self, assignment: dict[str, Any]) -> NodeExecutionResult:
        node_id = str(assignment.get("node_id", "UNKNOWN-NODE"))
        worker_id = str(assignment.get("worker_id", "UNKNOWN-WORKER"))
        plugin = str(assignment.get("plugin", "unknown"))
        action = str(assignment.get("action", "unknown"))
        return NodeExecutionResult(
            node_id=node_id,
            worker_id=worker_id,
            plugin=plugin,
            action=action,
            status="dry_run_complete",
            outputs=[f"dry-run://{node_id}"],
            message="Assignment simulated successfully.",
        )
