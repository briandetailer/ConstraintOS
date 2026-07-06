from pathlib import Path

import pytest
import yaml

from constraintos.constraint_pack import apply_constraint_pack
from constraintos.validation import ValidationEvidence, ValidationGate, ValidationIssueCode, ValidationKernel


CONSTRAINT_PACK_REFERENCE = {"id": "CPACK-0001", "version": "0.1", "title": "LF4 Engineering Atlas Constraint Pack"}


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


def test_validation_kernel_rejects_unknown_evidence_gate() -> None:
    with pytest.raises(ValueError, match="unknown gate: GATE-9999"):
        ValidationKernel().evaluate(
            gates=[{"id": "GATE-0001", "name": "Gate", "required_pass": True}],
            evidence=[{"gate_id": "GATE-9999", "status": "passed"}],
        )


def test_validation_kernel_rejects_duplicate_evidence_gate() -> None:
    with pytest.raises(ValueError, match="duplicate validation evidence for gate: GATE-0001"):
        ValidationKernel().evaluate(
            gates=[{"id": "GATE-0001", "name": "Gate", "required_pass": True}],
            evidence=[
                {"gate_id": "GATE-0001", "status": "passed"},
                {"gate_id": "GATE-0001", "status": "passed"},
            ],
        )


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


def test_validation_kernel_rejects_unknown_evidence_gate_for_render_specification() -> None:
    source = Path("examples/render/lf4_engine_render_specification.yaml")
    render_specification = yaml.safe_load(source.read_text(encoding="utf-8"))

    with pytest.raises(ValueError, match="unknown gate: GATE-9999"):
        ValidationKernel().evaluate_render_specification(
            render_specification,
            [{"gate_id": "GATE-9999", "status": "passed"}],
        )


def test_validation_kernel_includes_constraint_pack_references() -> None:
    render_source = Path("examples/render/lf4_engine_render_specification.yaml")
    pack_source = Path("examples/constraint_packs/lf4_engine_constraint_pack.yaml")
    render_specification = yaml.safe_load(render_source.read_text(encoding="utf-8"))
    constraint_pack = yaml.safe_load(pack_source.read_text(encoding="utf-8"))
    applied = apply_constraint_pack(render_specification, constraint_pack)

    report = ValidationKernel().evaluate_render_specification(applied, [])

    assert report.constraint_packs == [CONSTRAINT_PACK_REFERENCE]
    assert report.to_dict()["validation_report"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]


def test_validation_kernel_rejects_invalid_constraint_pack_references() -> None:
    render_specification = {
        "subject": {"id": "LF4-ENGINE"},
        "validation": {"gates": [{"id": "GATE-0001", "name": "Gate", "required_pass": True}]},
        "constraint_packs": {"id": "CPACK-0001"},
    }

    with pytest.raises(ValueError, match="constraint_packs must be a list"):
        ValidationKernel().evaluate_render_specification(render_specification, [])


def test_validation_kernel_rejects_non_object_constraint_pack_reference() -> None:
    render_specification = {
        "subject": {"id": "LF4-ENGINE"},
        "validation": {"gates": [{"id": "GATE-0001", "name": "Gate", "required_pass": True}]},
        "constraint_packs": ["CPACK-0001"],
    }

    with pytest.raises(ValueError, match="constraint_packs 1 must be an object"):
        ValidationKernel().evaluate_render_specification(render_specification, [])


def test_validation_kernel_rejects_constraint_pack_reference_without_id() -> None:
    render_specification = {
        "subject": {"id": "LF4-ENGINE"},
        "validation": {"gates": [{"id": "GATE-0001", "name": "Gate", "required_pass": True}]},
        "constraint_packs": [{"title": "Missing ID"}],
    }

    with pytest.raises(ValueError, match="constraint_packs 1 must include an id"):
        ValidationKernel().evaluate_render_specification(render_specification, [])


def test_validation_kernel_rejects_render_specification_without_gates() -> None:
    with pytest.raises(ValueError, match="validation gates"):
        ValidationKernel().evaluate_render_specification({"subject": {"id": "LF4-ENGINE"}, "validation": {"gates": []}})
