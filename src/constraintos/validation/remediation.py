from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

from constraintos.validation.failure_report import ValidationFailureReport


@dataclass(frozen=True)
class ValidationRemediationPlan:
    """Action plan produced from a validation failure report."""

    id: str
    failure_report_id: str | None
    status: str
    actions: list[dict[str, Any]] = field(default_factory=list)

    def required(self) -> bool:
        return self.status == "required"

    def to_dict(self) -> dict[str, Any]:
        return {
            "remediation_plan": {
                "id": self.id,
                "failure_report_id": self.failure_report_id,
                "status": self.status,
                "created": date.today().isoformat(),
                "action_count": len(self.actions),
            },
            "actions": self.actions,
        }


class ValidationRemediationPlanner:
    """Turns validation failures into deterministic remediation actions."""

    def build(
        self,
        failure_report: ValidationFailureReport | dict[str, Any],
        remediation_plan_id: str = "REMEDIATION-PLAN-0001",
    ) -> ValidationRemediationPlan:
        payload = failure_report.to_dict() if isinstance(failure_report, ValidationFailureReport) else failure_report
        header = payload.get("failure_report", {}) if isinstance(payload, dict) else {}
        failures = payload.get("failures", []) if isinstance(payload, dict) else []
        if not isinstance(failures, list):
            failures = []
        actions = [self._action_from_failure(index, failure) for index, failure in enumerate(failures, start=1) if isinstance(failure, dict)]
        return ValidationRemediationPlan(
            id=remediation_plan_id,
            failure_report_id=header.get("id") if isinstance(header, dict) else None,
            status="required" if actions else "not_required",
            actions=actions,
        )

    def _action_from_failure(self, index: int, failure: dict[str, Any]) -> dict[str, Any]:
        remediation = str(failure.get("remediation") or "Review and correct the validation issue.")
        return {
            "id": f"REMEDIATION-{index:04d}",
            "gate_id": failure.get("gate_id"),
            "gate_name": failure.get("gate_name"),
            "issue_code": failure.get("issue_code"),
            "severity": failure.get("severity"),
            "instruction": remediation,
            "source_reason": failure.get("reason", ""),
        }
