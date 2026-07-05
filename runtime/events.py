from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class RuntimeEvent:
    """Audit-friendly runtime event emitted during orchestration."""

    event_type: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type,
            "payload": self.payload,
        }


class RuntimeEventType:
    STARTED = "runtime_started"
    PLANNED = "runtime_planned"
    SCHEDULED = "runtime_scheduled"
    EXECUTION_STARTED = "runtime_execution_started"
    COMPLETED = "runtime_completed"
    FAILED = "runtime_failed"
