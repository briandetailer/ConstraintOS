from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

from constraintos.validation.models import ValidationReport


@dataclass(frozen=True)
class ValidationFailureReport:
    """Automation-ready summary of validation results that did not pass."""

    id: str
    validation_report_id: str | None
    status: str
    failures: list[dict[str, Any]] = field(default_factory=list)

    def has_failures(self) -> bool:
        return bool(self.failures)

    def to_dict(self) -> dict[str, Any]:
        return {
            "failure_report": {
                "id": self.id,
                "validation_report_id": self.validation_report_id,
                "status": self.status,
                "created": date.today().isoformat(),
                "failure_count": len(self.failures),
            },
            "failures": self.failures,
        }


class ValidationFailureReporter:
    """Extracts non-passing validation results into a focused failure report."""

    def build(
        self,
        validation_report: ValidationReport | dict[str, Any],
        failure_report_id: str = "FAILURE-REPORT-0001",
    ) -> ValidationFailureReport:
        report = validation_report.to_dict() if isinstance(validation_report, ValidationReport) else validation_report
        header = report.get("validation_report", {}) if isinstance(report, dict) else {}
        results = report.get("results", []) if isinstance(report, dict) else []
        if not isinstance(results, list):
            results = []
        failures = [self._failure_from_result(result) for result in results if self._is_failure(result)]
        return ValidationFailureReport(
            id=failure_report_id,
            validation_report_id=header.get("id") if isinstance(header, dict) else None,
            status="failed" if failures else "passed",
            failures=failures,
        )

    def _is_failure(self, result: Any) -> bool:
        return isinstance(result, dict) and result.get("status") != "passed"

    def _failure_from_result(self, result: dict[str, Any]) -> dict[str, Any]:
        issue_code = result.get("issue_code") if isinstance(result.get("issue_code"), dict) else {}
        return {
            "gate_id": result.get("gate_id"),
            "gate_name": result.get("name"),
            "status": result.get("status"),
            "required_pass": bool(result.get("required_pass", True)),
            "reason": result.get("reason", ""),
            "issue_code": issue_code.get("code"),
            "severity": issue_code.get("severity"),
            "remediation": issue_code.get("remediation"),
        }
