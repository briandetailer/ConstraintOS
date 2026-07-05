from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any


@dataclass(frozen=True)
class ExecutionRequest:
    id: str
    schedule_id: str
    assignments: list[dict[str, Any]]
    dry_run: bool = True

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
