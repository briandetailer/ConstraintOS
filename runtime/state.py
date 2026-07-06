from __future__ import annotations

from enum import Enum


class RuntimeState(str, Enum):
    """Lifecycle states for a runtime orchestration run."""

    PENDING = "pending"
    PLANNED = "planned"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"

    def terminal(self) -> bool:
        return self in {self.COMPLETED, self.PARTIAL, self.FAILED, self.CANCELLED, self.SKIPPED}

    def successful(self) -> bool:
        return self == self.COMPLETED
