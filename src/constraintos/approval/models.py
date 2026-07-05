from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any


@dataclass(frozen=True)
class ApprovalDecision:
    """Deterministic approval decision produced from validation results."""

    id: str
    artifact_id: str
    status: str
    summary: str
    reasons: list[str] = field(default_factory=list)
    validation_report_id: str | None = None

    def approved(self) -> bool:
        return self.status in {"approved", "approved_with_warnings"}

    def to_dict(self) -> dict[str, Any]:
        return {
            "approval": {
                "id": self.id,
                "created": date.today().isoformat(),
                "status": self.status,
            },
            "artifact": {
                "id": self.artifact_id,
                "validation_report_id": self.validation_report_id,
            },
            "decision": {
                "summary": self.summary,
                "reasons": self.reasons,
            },
        }
