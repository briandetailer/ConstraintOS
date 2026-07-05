from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

from constraintos.validation.remediation import ValidationRemediationPlan


@dataclass(frozen=True)
class ValidationRevisionRequest:
    """Request to revise an artifact based on remediation actions."""

    id: str
    artifact_id: str
    remediation_plan_id: str | None
    status: str
    steps: list[dict[str, Any]] = field(default_factory=list)

    def required(self) -> bool:
        return self.status == "revision_required"

    def to_dict(self) -> dict[str, Any]:
        return {
            "revision_request": {
                "id": self.id,
                "artifact_id": self.artifact_id,
                "remediation_plan_id": self.remediation_plan_id,
                "status": self.status,
                "created": date.today().isoformat(),
                "step_count": len(self.steps),
            },
            "steps": self.steps,
        }


class ValidationRevisionPlanner:
    """Builds a renderer-agnostic revision request from a remediation plan."""

    def build(
        self,
        remediation_plan: ValidationRemediationPlan | dict[str, Any],
        artifact_id: str = "UNKNOWN-ARTIFACT",
        revision_request_id: str = "REVISION-REQUEST-0001",
    ) -> ValidationRevisionRequest:
        payload = remediation_plan.to_dict() if isinstance(remediation_plan, ValidationRemediationPlan) else remediation_plan
        header = payload.get("remediation_plan", {}) if isinstance(payload, dict) else {}
        actions = payload.get("actions", []) if isinstance(payload, dict) else []
        if not isinstance(actions, list):
            actions = []
        steps = [self._step_from_action(index, action) for index, action in enumerate(actions, start=1) if isinstance(action, dict)]
        return ValidationRevisionRequest(
            id=revision_request_id,
            artifact_id=artifact_id,
            remediation_plan_id=header.get("id") if isinstance(header, dict) else None,
            status="revision_required" if steps else "not_required",
            steps=steps,
        )

    def _step_from_action(self, index: int, action: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": f"REVISION-STEP-{index:04d}",
            "remediation_action_id": action.get("id"),
            "gate_id": action.get("gate_id"),
            "issue_code": action.get("issue_code"),
            "severity": action.get("severity"),
            "instruction": action.get("instruction", "Review and revise artifact."),
            "source_reason": action.get("source_reason", ""),
        }
