from __future__ import annotations

from copy import deepcopy
from typing import Any

from constraintos.validation.models import (
    ValidationEvidence,
    ValidationGate,
    ValidationIssueCode,
    ValidationReport,
    ValidationResult,
)

MISSING_EVIDENCE = ValidationIssueCode(
    code="VAL-0001",
    title="Missing validation evidence",
    severity="blocker",
    remediation="Supply evidence for the required validation gate.",
)

GATE_EVIDENCE_FAILED = ValidationIssueCode(
    code="VAL-0002",
    title="Validation evidence did not pass",
    severity="blocker",
    remediation="Revise the artifact or provide corrected validation evidence.",
)


class ValidationKernel:
    """Deterministic evaluator for validation gates and supplied evidence."""

    def evaluate(
        self,
        gates: list[ValidationGate | dict[str, Any]],
        evidence: list[ValidationEvidence | dict[str, Any]] | None = None,
        subject_id: str = "UNKNOWN-SUBJECT",
        report_id: str = "VALIDATION-REPORT-0001",
        constraint_packs: list[dict[str, Any]] | None = None,
    ) -> ValidationReport:
        normalized_gates = [self._gate_from_input(gate) for gate in gates]
        evidence_by_gate = self._evidence_by_gate(normalized_gates, evidence or [])
        results = [self._evaluate_gate(gate, evidence_by_gate.get(gate.id)) for gate in normalized_gates]
        required_issues = [result for result in results if result.required_pass and not result.passed()]
        status = "passed" if not required_issues else "failed"
        return ValidationReport(
            id=report_id,
            subject_id=subject_id,
            status=status,
            results=results,
            messages=["Validation passed." if status == "passed" else "Validation failed required gates."],
            constraint_packs=deepcopy(constraint_packs or []),
        )

    def evaluate_render_specification(
        self,
        render_specification: dict[str, Any],
        evidence: list[ValidationEvidence | dict[str, Any]] | None = None,
        report_id: str = "VALIDATION-REPORT-0001",
    ) -> ValidationReport:
        subject = render_specification.get("subject", {})
        validation = render_specification.get("validation", {})
        gates = validation.get("gates", []) if isinstance(validation, dict) else []
        if not isinstance(subject, dict):
            subject = {}
        if not isinstance(gates, list) or not gates:
            raise ValueError("render specification must contain validation gates")
        return self.evaluate(
            gates=gates,
            evidence=evidence,
            subject_id=str(subject.get("id", "UNKNOWN-SUBJECT")),
            report_id=report_id,
            constraint_packs=self._constraint_pack_references(render_specification),
        )

    def _constraint_pack_references(self, render_specification: dict[str, Any]) -> list[dict[str, Any]]:
        constraint_packs = render_specification.get("constraint_packs", [])
        if not isinstance(constraint_packs, list):
            raise ValueError("render specification constraint_packs must be a list")
        references: list[dict[str, Any]] = []
        for index, item in enumerate(constraint_packs, start=1):
            if not isinstance(item, dict):
                raise ValueError(f"render specification constraint_packs {index} must be an object")
            pack_id = item.get("id")
            if not isinstance(pack_id, str) or not pack_id:
                raise ValueError(f"render specification constraint_packs {index} must include an id")
            references.append(deepcopy(item))
        return references

    def _evidence_by_gate(
        self,
        gates: list[ValidationGate],
        evidence: list[ValidationEvidence | dict[str, Any]],
    ) -> dict[str, ValidationEvidence]:
        gate_ids = {gate.id for gate in gates}
        evidence_by_gate: dict[str, ValidationEvidence] = {}
        for entry in evidence:
            item = self._evidence_from_input(entry)
            if item.gate_id not in gate_ids:
                raise ValueError(f"validation evidence references unknown gate: {item.gate_id}")
            if item.gate_id in evidence_by_gate:
                raise ValueError(f"duplicate validation evidence for gate: {item.gate_id}")
            evidence_by_gate[item.gate_id] = item
        return evidence_by_gate

    def _evaluate_gate(self, gate: ValidationGate, evidence: ValidationEvidence | None) -> ValidationResult:
        if evidence is None:
            return ValidationResult(
                gate_id=gate.id,
                name=gate.name,
                status="missing_evidence",
                required_pass=gate.required_pass,
                reason="No evidence was supplied for this gate.",
                evidence=None,
                issue_code=MISSING_EVIDENCE,
            )
        if evidence.passed():
            return ValidationResult(
                gate_id=gate.id,
                name=gate.name,
                status="passed",
                required_pass=gate.required_pass,
                reason=evidence.message or "Gate evidence passed.",
                evidence=evidence.to_dict(),
            )
        return ValidationResult(
            gate_id=gate.id,
            name=gate.name,
            status="failed",
            required_pass=gate.required_pass,
            reason=evidence.message or "Gate evidence failed.",
            evidence=evidence.to_dict(),
            issue_code=GATE_EVIDENCE_FAILED,
        )

    def _gate_from_input(self, gate: ValidationGate | dict[str, Any]) -> ValidationGate:
        if isinstance(gate, ValidationGate):
            return gate
        return ValidationGate(
            id=str(gate.get("id", "UNKNOWN-GATE")),
            name=str(gate.get("name", gate.get("id", "UNKNOWN-GATE"))),
            required_pass=bool(gate.get("required_pass", True)),
            metadata={key: value for key, value in gate.items() if key not in {"id", "name", "required_pass"}},
        )

    def _evidence_from_input(self, evidence: ValidationEvidence | dict[str, Any]) -> ValidationEvidence:
        if isinstance(evidence, ValidationEvidence):
            return evidence
        return ValidationEvidence(
            gate_id=str(evidence.get("gate_id", "UNKNOWN-GATE")),
            status=str(evidence.get("status", "unknown")),
            message=str(evidence.get("message", "")),
            details=dict(evidence.get("details", {})) if isinstance(evidence.get("details", {}), dict) else {},
        )
