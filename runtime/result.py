from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

from runtime.events import RuntimeEvent
from runtime.state import RuntimeState


@dataclass(frozen=True)
class RuntimeResult:
    """Top-level result returned by runtime orchestration."""

    id: str
    status: RuntimeState
    success: bool
    plan: dict[str, Any] | None = None
    schedule: dict[str, Any] | None = None
    execution: dict[str, Any] | None = None
    artifacts: dict[str, Any] | None = None
    events: list[RuntimeEvent] = field(default_factory=list)
    messages: list[str] = field(default_factory=list)

    def summary(self) -> dict[str, int]:
        return {
            "plan_nodes": self._count(self.plan, "nodes"),
            "plan_stages": self._count(self.plan, "stages"),
            "scheduled_assignments": self._count(self.schedule, "assignments"),
            "unscheduled_nodes": self._count(self.schedule, "unscheduled_nodes"),
            "node_results": self._count(self.execution, "node_results"),
            "artifacts": self._count(self.artifacts, "artifacts"),
            "events": len(self.events),
        }

    def to_dict(self) -> dict[str, Any]:
        data = {
            "runtime_result": {
                "id": self.id,
                "status": self.status.value,
                "success": self.success,
                "created": date.today().isoformat(),
            },
            "summary": self.summary(),
            "plan": self.plan,
            "schedule": self.schedule,
            "execution": self.execution,
            "events": [event.to_dict() for event in self.events],
            "messages": self.messages,
        }
        if self.artifacts is not None:
            data["artifacts"] = self.artifacts
        return data

    def _count(self, payload: dict[str, Any] | None, key: str) -> int:
        if not isinstance(payload, dict):
            return 0
        value = payload.get(key, [])
        return len(value) if isinstance(value, list) else 0
