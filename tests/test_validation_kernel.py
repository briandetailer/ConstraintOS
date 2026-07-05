from pathlib import Path

import pytest
import yaml

from constraintos.validation import ValidationEvidence, ValidationGate, ValidationKernel


def test_validation_kernel_passes_when_required_gates_have_passing_evidence() -> None:
    report = ValidationKernel().evaluate(
        gates=[ValidationGate("GATE-0001", "LF4 Specificity Gate")],
        evidence=[ValidationEvidence("GATE-0001", "passed", "LF4 geometry matched reference.")],
        subject_id="LF4-ENGINE",
    )

    assert report.passed() is True
    assert report.status == "passed"
    assert report.results[0].status == "passed"
    assert report.to_dict()["validation_report"]["subject_id"] == "LF4-ENGINE"


def test_validation_kernel_fails_required_gate_when_evidence_is_missing() -> None:
    report = ValidationKernel().evaluate(
        gates=[{"id": "GATE-0001", "name": "LF4 Specificity Gate", "required_pass": True}],
        evidence=[],
        subject_id="LF4-ENGINE",
    )

    assert report.passed() is False
    assert report.status == "failed"
    assert report.results[0].status == "missing_evidence"
    assert report.results[0].reason == "No evidence was supplied for this gate."


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
