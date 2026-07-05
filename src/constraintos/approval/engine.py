from __future__ import annotations

from typing import Any

from constraintos.approval.models import ApprovalDecision
from constraintos.validation import ValidationReport


class ApprovalEngine:
    """Applies deterministic approval policy to validation reports."""

    def decide(
        self,
        validation_report: ValidationReport | dict[str, Any],
        artifact_id: str = "UNKNOWN-ARTIFACT",
        decision_id: str = "APPROVAL-0001",
    ) -> ApprovalDecision:
        report = validation_report.to_dict() if isinstance(validation_report, ValidationReport) else validation_report
        report_header = report.get("validation_report", {})
        results = report.get("results", [])
        if not isinstance(results, list):
            results = []
        required_issues = [result for result in results if self._is_required_issue(result)]
        optional_issues = [result for result in results if self._is_optional_issue(result)]
        if required_issues:
            return ApprovalDecision(
                id=decision_id,
                artifact_id=artifact_id,
                status="rejected",
                summary="Rejected because required validation gates did not pass.",
                reasons=[self._reason_for(result) for result in required_issues],
                validation_report_id=report_header.get("id"),
            )
        if optional_issues:
            return ApprovalDecision(
                id=decision_id,
                artifact_id=artifact_id,
                status="approved_with_warnings",
                summary="Approved with warnings because only optional validation gates failed.",
                reasons=[self._reason_for(result) for result in optional_issues],
                validation_report_id=report_header.get("id"),
            )
        return ApprovalDecision(
            id=decision_id,
            artifact_id=artifact_id,
            status="approved",
            summary="Approved because all validation gates passed.",
            validation_report_id=report_header.get("id"),
        )

    def _is_required_issue(self, result: Any) -> bool:
        return isinstance(result, dict) and bool(result.get("required_pass", True)) and result.get("status") != "passed"

    def _is_optional_issue(self, result: Any) -> bool:
        return isinstance(result, dict) and not bool(result.get("required_pass", True)) and result.get("status") != "passed"

    def _reason_for(self, result: dict[str, Any]) -> str:
        issue_code = result.get("issue_code")
        if isinstance(issue_code, dict) and issue_code.get("code"):
            return f"{issue_code.get('code')}: {result.get('reason', '')}".rstrip()
        return str(result.get("reason") or result.get("name") or result.get("gate_id") or "Validation gate did not pass.")
