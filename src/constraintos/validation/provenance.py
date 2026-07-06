from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import date
from typing import Any

from constraintos.approval import ApprovalDecision
from constraintos.validation.failure_report import ValidationFailureReport
from constraintos.validation.models import ValidationReport
from constraintos.validation.remediation import ValidationRemediationPlan
from constraintos.validation.revision import ValidationRevisionRequest


@dataclass(frozen=True)
class ValidationProvenanceManifest:
    """Traceability manifest for one validation approval pipeline execution."""

    id: str
    subject_id: str
    artifact_id: str
    validation_report_id: str | None
    validation_status: str
    failure_report_id: str | None
    failure_status: str
    remediation_plan_id: str | None
    remediation_status: str
    revision_request_id: str | None
    revision_status: str
    approval_decision_id: str | None
    approval_status: str
    gates: list[dict[str, Any]] = field(default_factory=list)
    constraint_packs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        nodes = [
            {
                "type": "validation_report",
                "id": self.validation_report_id,
                "status": self.validation_status,
                "references": {"subject_id": self.subject_id},
            },
            {
                "type": "failure_report",
                "id": self.failure_report_id,
                "status": self.failure_status,
                "references": {"validation_report_id": self.validation_report_id},
            },
            {
                "type": "remediation_plan",
                "id": self.remediation_plan_id,
                "status": self.remediation_status,
                "references": {"failure_report_id": self.failure_report_id},
            },
            {
                "type": "revision_request",
                "id": self.revision_request_id,
                "status": self.revision_status,
                "references": {
                    "artifact_id": self.artifact_id,
                    "remediation_plan_id": self.remediation_plan_id,
                },
            },
            {
                "type": "approval_decision",
                "id": self.approval_decision_id,
                "status": self.approval_status,
                "references": {
                    "artifact_id": self.artifact_id,
                    "validation_report_id": self.validation_report_id,
                },
            },
        ]
        return {
            "provenance_manifest": {
                "id": self.id,
                "created": date.today().isoformat(),
                "status": self.approval_status,
                "source": "validation_approval_pipeline",
                "constraint_packs": deepcopy(self.constraint_packs),
            },
            "subject": {"id": self.subject_id},
            "artifact": {"id": self.artifact_id},
            "validation": {
                "report_id": self.validation_report_id,
                "status": self.validation_status,
                "result_count": len(self.gates),
            },
            "traceability": {
                "nodes": nodes,
                "gates": deepcopy(self.gates),
            },
        }


class ValidationProvenanceManifestBuilder:
    """Builds a deterministic provenance manifest from validation pipeline outputs."""

    def build(
        self,
        validation_report: ValidationReport | dict[str, Any],
        failure_report: ValidationFailureReport | dict[str, Any],
        remediation_plan: ValidationRemediationPlan | dict[str, Any],
        revision_request: ValidationRevisionRequest | dict[str, Any],
        approval_decision: ApprovalDecision | dict[str, Any],
        artifact_id: str = "UNKNOWN-ARTIFACT",
        provenance_manifest_id: str = "PROVENANCE-0001",
    ) -> ValidationProvenanceManifest:
        validation_payload = validation_report.to_dict() if isinstance(validation_report, ValidationReport) else validation_report
        failure_payload = failure_report.to_dict() if isinstance(failure_report, ValidationFailureReport) else failure_report
        remediation_payload = remediation_plan.to_dict() if isinstance(remediation_plan, ValidationRemediationPlan) else remediation_plan
        revision_payload = revision_request.to_dict() if isinstance(revision_request, ValidationRevisionRequest) else revision_request
        approval_payload = approval_decision.to_dict() if isinstance(approval_decision, ApprovalDecision) else approval_decision

        validation_header = validation_payload.get("validation_report", {}) if isinstance(validation_payload, dict) else {}
        failure_header = failure_payload.get("failure_report", {}) if isinstance(failure_payload, dict) else {}
        remediation_header = remediation_payload.get("remediation_plan", {}) if isinstance(remediation_payload, dict) else {}
        revision_header = revision_payload.get("revision_request", {}) if isinstance(revision_payload, dict) else {}
        approval_header = approval_payload.get("approval", {}) if isinstance(approval_payload, dict) else {}
        validation_header = validation_header if isinstance(validation_header, dict) else {}
        failure_header = failure_header if isinstance(failure_header, dict) else {}
        remediation_header = remediation_header if isinstance(remediation_header, dict) else {}
        revision_header = revision_header if isinstance(revision_header, dict) else {}
        approval_header = approval_header if isinstance(approval_header, dict) else {}

        results = validation_payload.get("results", []) if isinstance(validation_payload, dict) else []
        if not isinstance(results, list):
            results = []
        constraint_packs = validation_header.get("constraint_packs", [])
        if not isinstance(constraint_packs, list):
            constraint_packs = []

        return ValidationProvenanceManifest(
            id=provenance_manifest_id,
            subject_id=str(validation_header.get("subject_id", "UNKNOWN-SUBJECT")),
            artifact_id=artifact_id,
            validation_report_id=validation_header.get("id"),
            validation_status=str(validation_header.get("status", "unknown")),
            failure_report_id=failure_header.get("id"),
            failure_status=str(failure_header.get("status", "unknown")),
            remediation_plan_id=remediation_header.get("id"),
            remediation_status=str(remediation_header.get("status", "unknown")),
            revision_request_id=revision_header.get("id"),
            revision_status=str(revision_header.get("status", "unknown")),
            approval_decision_id=approval_header.get("id"),
            approval_status=str(approval_header.get("status", "unknown")),
            gates=[self._gate_trace(result) for result in results if isinstance(result, dict)],
            constraint_packs=[deepcopy(item) for item in constraint_packs if isinstance(item, dict)],
        )

    def _gate_trace(self, result: dict[str, Any]) -> dict[str, Any]:
        evidence = result.get("evidence") if isinstance(result.get("evidence"), dict) else {}
        issue_code = result.get("issue_code") if isinstance(result.get("issue_code"), dict) else {}
        return {
            "gate_id": result.get("gate_id"),
            "gate_name": result.get("name"),
            "status": result.get("status"),
            "required_pass": bool(result.get("required_pass", True)),
            "evidence_status": evidence.get("status"),
            "issue_code": issue_code.get("code"),
        }
