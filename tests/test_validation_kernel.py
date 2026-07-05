from pathlib import Path

import pytest
import yaml

from constraintos.validation import ValidationEvidence, ValidationGate, ValidationIssueCode, ValidationKernel


def test_validation_issue_code_serializes() -> None:
    code = ValidationIssueCode("VAL-0001", "Missing validation evidence", "blocker", "Supply evidence.")

    assert code.to_dict() == {
        "code": "VAL-0001",
        "title": "Missing validation evidence",
        "severity": "blocker",
        "remediation": "Supply evidence.",
    }


def test_validation_kernel_passes_when_required_gates_have_passing_evidence() -> None:
    report = ValidationKernel().evaluate(
        gates=[ValidationGate("GATE-0001", "LF4 Specificity Gate")],
        evidence=[ValidationEvidence("GATE-0001", "passed", "LF4 geometry matched reference.")],
        subject_id="LF4-ENGINE",
    )

    assert report.passed() is True
    assert report.status == "passed"
    assert report.results[0].status == "passed"
    assert report.results[0].issue_code is None
    assert report.to_dict()["validation_report"]["subject_id"] == "LF4-ENGINE"


def test_validation_kernel_fails_required_gate_when_evidence_is_missing() -> None:
    report = ValidationKernel().evaluate(
        gates=[{"id": "GATE-0001", "name": "LF4 Specificity Gate", "required_pass": True}],
        evidence=[],
        subject_id="LF4-ENGINE",
    )

    result = report.results[0]
    assert report.passed() is False
    assert report.status == "failed"
    assert result.status == "missing_evidence"
    assert result.reason == "No evidence was supplied for this gate."
    assert result.issue_code is not None
    assert result.issue_code.code == "VAL-0001"
    assert result.to_dict()["issue_code"]["remediation"] == "Supply evidence for the required validation gate."


def test_validation_kernel_attaches_issue_code_when_evidence_fails() -> None:
    report = ValidationKernel().evaluate(
        gates=[{"id": "GATE-0001", "name": "LF4 Specificity Gate", "required_pass": True}],
        evidence=[{"gate_id": "GATE-0001", "status": "failed", "message": "Geometry mismatch."}],
    )

    result = report.results[0]
    assert report.status == "failed"
    assert result.status == "failed"
    assert result.issue_code is not None
    assert result.issue_code.code == "VAL-0002"
    assert result.to_dict()["issue_code"]["title"] == "Validation evidence did not pass"


def test_validation_kernel_does_not_fail_report_for_optional_gate_failure() -> None:
    report = ValidationKernel().evaluate(
        gates=[{"id": "GATE-0001", "name": "Advisory Gate", "required_pass": False}],
        evidence=[{"gate_id": "GATE-0001", "status": "failed", "message": "Advisory note failed."}],
    )

    assert report.passed() is True
    assert report.results[0].status == "failed"


def test_validation_kernel_evaluates_render_specification_gates() -> None:
    source = Path("examples/render/lf4_engine_render_specification.yaml")
    render_specification = yaml.safe_load(source.read_text(encoding="utf-8"))
    evidence = [
        {"gate_id": "GATE-0001", "status": "passed", "message": "LF4 specificity passed."},
        {"gate_id": "GATE-0002", "status": "passed", "message": "Mechanical plausibility passed."},
        {"gate_id": "GATE-0003", "status": "passed", "message": "Schematic continuation passed."},
    ]

    report = ValidationKernel().evaluate_render_specification(render_specification, evidence)

    assert report.passed() is True
    assert report.subject_id == "LF4-ENGINE"
    assert [result.gate_id for result in report.results] == ["GATE-0001", "GATE-0002", "GATE-0003"]


def test_validation_kernel_rejects_render_specification_without_gates() -> None:
    with pytest.raises(ValueError, match="validation gates"):
        ValidationKernel().evaluate_render_specification({"subject": {"id": "LF4-ENGINE"}, "validation": {"gates": []}})
