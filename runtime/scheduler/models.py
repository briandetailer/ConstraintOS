from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any


@dataclass(frozen=True)
class WorkerCapability:
    worker_id: str
    plugins: list[str]
    status: str = "available"

    def supports(self, plugin: str) -> bool:
        return self.status == "available" and plugin in self.plugins

    def to_dict(self) -> dict[str, Any]:
        return {
            "worker_id": self.worker_id,
            "plugins": self.plugins,
            "status": self.status,
        }


@dataclass(frozen=True)
class ScheduledAssignment:
    node_id: str
    stage_id: str
    worker_id: str
    plugin: str
    action: str

    def to_dict(self) -> dict[str, str]:
        return {
            "node_id": self.node_id,
            "stage_id": self.stage_id,
            "worker_id": self.worker_id,
            "plugin": self.plugin,
            "action": self.action,
        }


@dataclass(frozen=True)
class ScheduleResult:
    id: str
    plan_id: str
    status: str
    assignments: list[ScheduledAssignment]
    unscheduled_nodes: list[str] = field(default_factory=list)
    messages: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schedule_result": {
                "id": self.id,
                "plan_id": self.plan_id,
                "status": self.status,
                "created": date.today().isoformat(),
            },
            "assignments": [assignment.to_dict() for assignment in self.assignments],
            "unscheduled_nodes": self.unscheduled_nodes,
            "messages": self.messages,
        }
