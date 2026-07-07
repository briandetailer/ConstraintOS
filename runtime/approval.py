from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


VALID_APPROVAL_DECISIONS = {"approved", "rejected", "needs_review", "waived"}
VALID_APPROVAL_CHECK_STATUSES = {"passed", "failed", "waived", "needs_review"}
REQUIRED_APPROVAL_FIELDS = (
    "runtime_id",
    "evidence_manifest_artifact_id",
    "decision",
    "decided_by",
    "decided_at",
    "approval_policy",
)
REQUIRED_APPROVAL_CHECK_FIELDS = ("id", "name", "status", "source")


@dataclass(frozen=True)
class RuntimeApprovalVerification:
    issues: list[str] = field(default_factory=list)

    def successful(self) -> bool:
        return not self.issues

    def to_dict(self) -> dict[str, Any]:
        return {
            "runtime_approval_verification": {
                "successful": self.successful(),
                "issue_count": len(self.issues),
            },
            "issues": self.issues,
        }


def verify_runtime_approval_decision(decision: dict[str, Any]) -> RuntimeApprovalVerification:
    """Verify a Runtime approval decision payload without mutating the payload."""
    if not isinstance(decision, dict):
        return RuntimeApprovalVerification(["Runtime approval decision must be a dictionary."])

    issues: list[str] = []
    approval = _dict_value(decision, "runtime_approval")
    checks = decision.get("checks", [])
    notes = decision.get("notes", [])

    for field_name in REQUIRED_APPROVAL_FIELDS:
        if not approval.get(field_name):
            issues.append(f"Runtime approval requires {field_name}.")

    decision_value = approval.get("decision")
    if decision_value and decision_value not in VALID_APPROVAL_DECISIONS:
        issues.append("Runtime approval decision must be approved, rejected, needs_review, or waived.")

    if not isinstance(checks, list):
        issues.append("Runtime approval checks must be a list.")
        checks = []
    if not isinstance(notes, list):
        issues.append("Runtime approval notes must be a list.")
        notes = []
    elif not all(isinstance(note, str) and note for note in notes):
        issues.append("Runtime approval notes must be non-empty strings.")

    failed_checks = 0
    waived_checks = 0
    for index, check in enumerate(checks, start=1):
        if not isinstance(check, dict):
            issues.append(f"Runtime approval check {index} must be a dictionary.")
            continue
        for field_name in REQUIRED_APPROVAL_CHECK_FIELDS:
            if not check.get(field_name):
                issues.append(f"Runtime approval check {index} requires {field_name}.")
        status = check.get("status")
        if status and status not in VALID_APPROVAL_CHECK_STATUSES:
            issues.append(f"Runtime approval check {index} status must be passed, failed, waived, or needs_review.")
        if status == "failed":
            failed_checks += 1
        if status == "waived":
            waived_checks += 1
        if "message" in check and not isinstance(check.get("message"), str):
            issues.append(f"Runtime approval check {index} message must be a string.")
        if "metadata" in check and not isinstance(check.get("metadata"), dict):
            issues.append(f"Runtime approval check {index} metadata must be a dictionary.")

    if decision_value == "rejected" and failed_checks == 0 and not notes:
        issues.append("Rejected runtime approval decisions require a failed check or explanatory note.")
    if decision_value == "waived" and waived_checks == 0 and not notes:
        issues.append("Waived runtime approval decisions require a waived check or explanatory note.")

    return RuntimeApprovalVerification(issues)


def _dict_value(value: dict[str, Any], key: str) -> dict[str, Any]:
    payload = value.get(key, {}) if isinstance(value, dict) else {}
    return payload if isinstance(payload, dict) else {}
