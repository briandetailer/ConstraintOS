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
    constraint_packs: list[dict[str, Any]] = field(default_factory=list)

    def approved(self) -> bool:
        return self.status in {"approved", "approved_with_warnings"}

    def to_dict(self) -> dict[str, Any]:
        return {
            "approval": {
                "id": self.id,
                "created": date.today().isoformat(),
                "status": self.status,
                "constraint_packs": self.constraint_packs,
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
