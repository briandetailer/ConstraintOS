from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any

from constraintos.approval import ApprovalDecision, ApprovalEngine
from constraintos.validation.failure_report import ValidationFailureReport, ValidationFailureReporter
from constraintos.validation.kernel import ValidationKernel
from constraintos.validation.models import ValidationEvidence, ValidationReport
from constraintos.validation.provenance import ValidationProvenanceManifest, ValidationProvenanceManifestBuilder
from constraintos.validation.remediation import ValidationRemediationPlan, ValidationRemediationPlanner
from constraintos.validation.revision import ValidationRevisionPlanner, ValidationRevisionRequest


@dataclass(frozen=True)
class ValidationApprovalResult:
    validation_report: ValidationReport
    approval_decision: ApprovalDecision
    failure_report: ValidationFailureReport
    remediation_plan: ValidationRemediationPlan
    revision_request: ValidationRevisionRequest
    provenance_manifest: ValidationProvenanceManifest
    constraint_packs: list[dict[str, Any]] = field(default_factory=list)

    def approved(self) -> bool:
        return self.approval_decision.approved()

    def to_dict(self) -> dict[str, Any]:
        return {
            "constraint_packs": deepcopy(self.constraint_packs),
            "provenance_manifest": self.provenance_manifest.to_dict(),
            "validation": self.validation_report.to_dict(),
            "failure_report": self.failure_report.to_dict(),
            "remediation_plan": self.remediation_plan.to_dict(),
            "revision_request": self.revision_request.to_dict(),
            "approval": self.approval_decision.to_dict(),
        }


class ValidationApprovalPipeline:
    def __init__(
        self,
        kernel: ValidationKernel | None = None,
        approval_engine: ApprovalEngine | None = None,
        failure_reporter: ValidationFailureReporter | None = None,
        remediation_planner: ValidationRemediationPlanner | None = None,
        revision_planner: ValidationRevisionPlanner | None = None,
        provenance_builder: ValidationProvenanceManifestBuilder | None = None,
    ) -> None:
        self.kernel = kernel or ValidationKernel()
        self.approval_engine = approval_engine or ApprovalEngine()
        self.failure_reporter = failure_reporter or ValidationFailureReporter()
        self.remediation_planner = remediation_planner or ValidationRemediationPlanner()
        self.revision_planner = revision_planner or ValidationRevisionPlanner()
        self.provenance_builder = provenance_builder or ValidationProvenanceManifestBuilder()

    def evaluate_render_specification(
        self,
        render_specification: dict[str, Any],
        evidence: list[ValidationEvidence | dict[str, Any]] | None = None,
        artifact_id: str = "UNKNOWN-ARTIFACT",
        validation_report_id: str = "VALIDATION-REPORT-0001",
        approval_decision_id: str = "APPROVAL-0001",
        failure_report_id: str = "FAILURE-REPORT-0001",
        remediation_plan_id: str = "REMEDIATION-PLAN-0001",
        revision_request_id: str = "REVISION-REQUEST-0001",
        provenance_manifest_id: str | None = None,
    ) -> ValidationApprovalResult:
        validation_report = self.kernel.evaluate_render_specification(
            render_specification,
            evidence=evidence,
            report_id=validation_report_id,
        )
        failure_report = self.failure_reporter.build(validation_report, failure_report_id=failure_report_id)
        remediation_plan = self.remediation_planner.build(failure_report, remediation_plan_id=remediation_plan_id)
        revision_request = self.revision_planner.build(
            remediation_plan,
            artifact_id=artifact_id,
            revision_request_id=revision_request_id,
        )
        approval_decision = self.approval_engine.decide(
            validation_report,
            artifact_id=artifact_id,
            decision_id=approval_decision_id,
        )
        provenance_manifest = self.provenance_builder.build(
            validation_report=validation_report,
            failure_report=failure_report,
            remediation_plan=remediation_plan,
            revision_request=revision_request,
            approval_decision=approval_decision,
            artifact_id=artifact_id,
            provenance_manifest_id=provenance_manifest_id,
        )
        return ValidationApprovalResult(
            validation_report=validation_report,
            approval_decision=approval_decision,
            failure_report=failure_report,
            remediation_plan=remediation_plan,
            revision_request=revision_request,
            provenance_manifest=provenance_manifest,
            constraint_packs=deepcopy(validation_report.constraint_packs),
        )
