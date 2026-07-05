from pathlib import Path

import yaml

from constraintos.validation import ValidationApprovalPipeline


def load_lf4_specification() -> dict:
    source = Path("examples/render/lf4_engine_render_specification.yaml")
    return yaml.safe_load(source.read_text(encoding="utf-8"))


def passing_evidence() -> list[dict[str, str]]:
    return [
        {"gate_id": "GATE-0001", "status": "passed", "message": "LF4 specificity passed."},
        {"gate_id": "GATE-0002", "status": "passed", "message": "Mechanical plausibility passed."},
        {"gate_id": "GATE-0003", "status": "passed", "message": "Schematic continuation passed."},
    ]


def test_validation_approval_pipeline_approves_passing_render_specification() -> None:
    result = ValidationApprovalPipeline().evaluate_render_specification(
        load_lf4_specification(),
        evidence=passing_evidence(),
        artifact_id="ARTIFACT-0001",
    )

    assert result.approved() is True
    assert result.validation_report.status == "passed"
    assert result.approval_decision.status == "approved"


def test_validation_approval_pipeline_rejects_missing_required_evidence() -> None:
    result = ValidationApprovalPipeline().evaluate_render_specification(
        load_lf4_specification(),
        evidence=passing_evidence()[:2],
        artifact_id="ARTIFACT-0001",
    )

    assert result.approved() is False
    assert result.validation_report.status == "failed"
    assert result.approval_decision.status == "rejected"
    assert result.approval_decision.reasons == ["VAL-0001: No evidence was supplied for this gate."]


def test_validation_approval_pipeline_serializes_combined_result() -> None:
    payload = ValidationApprovalPipeline().evaluate_render_specification(
        load_lf4_specification(),
        evidence=passing_evidence(),
        artifact_id="ARTIFACT-0001",
        validation_report_id="VALIDATION-REPORT-0007",
        approval_decision_id="APPROVAL-0007",
    ).to_dict()

    assert payload["validation"]["validation_report"]["id"] == "VALIDATION-REPORT-0007"
    assert payload["approval"]["approval"]["id"] == "APPROVAL-0007"
    assert payload["approval"]["artifact"]["id"] == "ARTIFACT-0001"
