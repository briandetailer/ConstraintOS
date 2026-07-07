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
REQUIRED_POLICY_HEADER_FIELDS = ("name", "version", "contract_registry_version")
REQUIRED_POLICY_LISTS = (
    "required_evidence_artifacts",
    "required_checks",
    "allowed_decisions",
    "allowed_check_statuses",
    "approvers",
)
REQUIRED_EVIDENCE_ARTIFACT_ROLES = {
    "runtime_report",
    "runtime_trace_report",
    "runtime_contract_registry",
    "runtime_evidence_manifest",
}


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


def verify_runtime_approval_policy(policy: dict[str, Any]) -> RuntimeApprovalVerification:
    """Verify a Runtime approval policy payload without mutating the payload."""
    if not isinstance(policy, dict):
        return RuntimeApprovalVerification(["Runtime approval policy must be a dictionary."])

    issues: list[str] = []
    policy_header = _dict_value(policy, "runtime_approval_policy")
    for field_name in REQUIRED_POLICY_HEADER_FIELDS:
        if not policy_header.get(field_name):
            issues.append(f"Runtime approval policy requires {field_name}.")

    for field_name in REQUIRED_POLICY_LISTS:
        _validate_non_empty_string_list(policy, field_name, issues)

    allowed_decisions = policy.get("allowed_decisions", [])
    if isinstance(allowed_decisions, list):
        for decision in allowed_decisions:
            if decision not in VALID_APPROVAL_DECISIONS:
                issues.append("Runtime approval policy allowed_decisions must contain only supported decisions.")
                break

    allowed_check_statuses = policy.get("allowed_check_statuses", [])
    if isinstance(allowed_check_statuses, list):
        for status in allowed_check_statuses:
            if status not in VALID_APPROVAL_CHECK_STATUSES:
                issues.append("Runtime approval policy allowed_check_statuses must contain only supported check statuses.")
                break

    required_artifacts_value = policy.get("required_evidence_artifacts", [])
    required_artifacts = set(required_artifacts_value) if isinstance(required_artifacts_value, list) else set()
    missing_artifacts = sorted(REQUIRED_EVIDENCE_ARTIFACT_ROLES - required_artifacts)
    if missing_artifacts:
        issues.append("Runtime approval policy must require all Runtime evidence artifact roles.")

    waiver_rules = _dict_value(policy, "waiver_rules")
    rejection_rules = _dict_value(policy, "rejection_rules")
    _validate_bool_rule(waiver_rules, "requires_note_or_waived_check", "waiver_rules", issues)
    _validate_bool_rule(rejection_rules, "requires_note_or_failed_check", "rejection_rules", issues)

    return RuntimeApprovalVerification(issues)


def _dict_value(value: dict[str, Any], key: str) -> dict[str, Any]:
    payload = value.get(key, {}) if isinstance(value, dict) else {}
    return payload if isinstance(payload, dict) else {}


def _validate_non_empty_string_list(value: dict[str, Any], key: str, issues: list[str]) -> None:
    items = value.get(key)
    if not isinstance(items, list) or not items:
        issues.append(f"Runtime approval policy {key} must be a non-empty list.")
        return
    if not all(isinstance(item, str) and item for item in items):
        issues.append(f"Runtime approval policy {key} must contain non-empty strings.")


def _validate_bool_rule(rules: dict[str, Any], key: str, label: str, issues: list[str]) -> None:
    if rules.get(key) is not True:
        issues.append(f"Runtime approval policy {label}.{key} must be true.")
