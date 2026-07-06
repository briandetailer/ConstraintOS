from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any


class ExecutionRequestBuildError(ValueError):
    """Raised when an execution request cannot be built from a schedule."""


@dataclass(frozen=True)
class ExecutionRequest:
    id: str
    schedule_id: str
    assignments: list[dict[str, Any]]
    dry_run: bool = True

    @classmethod
    def from_schedule(
        cls,
        schedule: dict[str, Any],
        request_id: str = "EXEC-REQ-0001",
        dry_run: bool = True,
        allow_partial: bool = False,
    ) -> "ExecutionRequest":
        schedule_meta = schedule.get("schedule_result", {}) if isinstance(schedule, dict) else {}
        if not isinstance(schedule_meta, dict):
            schedule_meta = {}
        status = str(schedule_meta.get("status", "unknown"))
        if status != "scheduled" and not allow_partial:
            raise ExecutionRequestBuildError("Cannot build execution request from partial schedule")
        assignments = schedule.get("assignments", []) if isinstance(schedule, dict) else []
        if not isinstance(assignments, list):
            raise ExecutionRequestBuildError("schedule assignments must be a list")
        return cls(
            id=request_id,
            schedule_id=str(schedule_meta.get("id", "UNKNOWN-SCHEDULE")),
            assignments=[assignment for assignment in assignments if isinstance(assignment, dict)],
            dry_run=dry_run,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_request": {
                "id": self.id,
                "schedule_id": self.schedule_id,
                "dry_run": self.dry_run,
                "created": date.today().isoformat(),
            },
            "assignments": self.assignments,
        }


@dataclass(frozen=True)
class NodeExecutionResult:
    node_id: str
    worker_id: str
    plugin: str
    action: str
    status: str
    outputs: list[str] = field(default_factory=list)
    message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "worker_id": self.worker_id,
            "plugin": self.plugin,
            "action": self.action,
            "status": self.status,
            "outputs": self.outputs,
            "message": self.message,
        }


@dataclass(frozen=True)
class ExecutionResult:
    id: str
    request_id: str
    status: str
    node_results: list[NodeExecutionResult]
    messages: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_result": {
                "id": self.id,
                "request_id": self.request_id,
                "status": self.status,
                "created": date.today().isoformat(),
            },
            "node_results": [result.to_dict() for result in self.node_results],
            "messages": self.messages,
        }
