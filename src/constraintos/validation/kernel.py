from __future__ import annotations

from typing import Any

from constraintos.validation.models import ValidationEvidence, ValidationGate, ValidationReport, ValidationResult


class ValidationKernel:
    """Deterministic evaluator for validation gates and supplied evidence."""

    def evaluate(
        self,
        gates: list[ValidationGate | dict[str, Any]],
        evidence: list[ValidationEvidence | dict[str, Any]] | None = None,
        subject_id: str = "UNKNOWN-SUBJECT",
        report_id: str = "VALIDATION-REPORT-0001",
    ) -> ValidationReport:
        normalized_gates = [self._gate_from_input(gate) for gate in gates]
        evidence_by_gate = {item.gate_id: item for item in [self._evidence_from_input(entry) for entry in (evidence or [])]}
        results = [self._evaluate_gate(gate, evidence_by_gate.get(gate.id)) for gate in normalized_gates]
        required_failures = [result for result in results if result.required_pass and not result.passed()]
        status = "passed" if not required_failures else "failed"
        return ValidationReport(
            id=report_id,
            subject_id=subject_id,
            status=status,
            results=results,
            messages=["Validation passed." if status == "passed" else "Validation failed required gates."],
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
        )

    def _evaluate_gate(self, gate: ValidationGate, evidence: ValidationEvidence | None) -> ValidationResult:
        if evidence is None:
            return ValidationResult(
                gate_id=gate.id,
                name=gate.name,
                status="missing_evidence",
                required_pass=gate.required_pass,
                reason="No evidence was supplied for this gate.",
                evidence=None,
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
