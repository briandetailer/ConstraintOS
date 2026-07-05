from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from constraintos.approval import ApprovalDecision, ApprovalEngine
from constraintos.validation.failure_report import ValidationFailureReport, ValidationFailureReporter
from constraintos.validation.kernel import ValidationKernel
from constraintos.validation.models import ValidationEvidence, ValidationReport


@dataclass(frozen=True)
class ValidationApprovalResult:
    validation_report: ValidationReport
    approval_decision: ApprovalDecision
    failure_report: ValidationFailureReport

    def approved(self) -> bool:
        return self.approval_decision.approved()

    def to_dict(self) -> dict[str, Any]:
        return {
            "validation": self.validation_report.to_dict(),
            "failure_report": self.failure_report.to_dict(),
            "approval": self.approval_decision.to_dict(),
        }


class ValidationApprovalPipeline:
    def __init__(
        self,
        kernel: ValidationKernel | None = None,
        approval_engine: ApprovalEngine | None = None,
        failure_reporter: ValidationFailureReporter | None = None,
    ) -> None:
        self.kernel = kernel or ValidationKernel()
        self.approval_engine = approval_engine or ApprovalEngine()
        self.failure_reporter = failure_reporter or ValidationFailureReporter()

    def evaluate_render_specification(
        self,
        render_specification: dict[str, Any],
        evidence: list[ValidationEvidence | dict[str, Any]] | None = None,
        artifact_id: str = "UNKNOWN-ARTIFACT",
        validation_report_id: str = "VALIDATION-REPORT-0001",
        approval_decision_id: str = "APPROVAL-0001",
        failure_report_id: str = "FAILURE-REPORT-0001",
    ) -> ValidationApprovalResult:
        validation_report = self.kernel.evaluate_render_specification(
            render_specification,
            evidence=evidence,
            report_id=validation_report_id,
        )
        failure_report = self.failure_reporter.build(validation_report, failure_report_id=failure_report_id)
        approval_decision = self.approval_engine.decide(
            validation_report,
            artifact_id=artifact_id,
            decision_id=approval_decision_id,
        )
        return ValidationApprovalResult(
            validation_report=validation_report,
            approval_decision=approval_decision,
            failure_report=failure_report,
        )
