from pathlib import Path

import yaml

from constraintos.constraint_pack import apply_constraint_pack
from constraintos.validation import ValidationApprovalPipeline


CONSTRAINT_PACK_REFERENCE = {"id": "CPACK-0001", "version": "0.1", "title": "LF4 Engineering Atlas Constraint Pack"}


def load_lf4_specification() -> dict:
    source = Path("examples/render/lf4_engine_render_specification.yaml")
    return yaml.safe_load(source.read_text(encoding="utf-8"))


def load_lf4_constraint_pack() -> dict:
    source = Path("examples/constraint_packs/lf4_engine_constraint_pack.yaml")
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


def test_validation_approval_pipeline_preserves_constraint_pack_traceability() -> None:
    render_specification = apply_constraint_pack(load_lf4_specification(), load_lf4_constraint_pack())

    payload = ValidationApprovalPipeline().evaluate_render_specification(
        render_specification,
        evidence=passing_evidence(),
        artifact_id="ARTIFACT-0001",
    ).to_dict()

    assert payload["validation"]["validation_report"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
    assert payload["failure_report"]["failure_report"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
    assert payload["remediation_plan"]["remediation_plan"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
    assert payload["revision_request"]["revision_request"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
    assert payload["approval"]["approval"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]


def test_validation_approval_pipeline_preserves_constraint_pack_traceability_when_rejected() -> None:
    render_specification = apply_constraint_pack(load_lf4_specification(), load_lf4_constraint_pack())

    payload = ValidationApprovalPipeline().evaluate_render_specification(
        render_specification,
        evidence=[],
        artifact_id="ARTIFACT-0001",
    ).to_dict()

    assert payload["validation"]["validation_report"]["status"] == "failed"
    assert payload["approval"]["approval"]["status"] == "rejected"
    assert payload["failure_report"]["failure_report"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
    assert payload["remediation_plan"]["remediation_plan"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
    assert payload["revision_request"]["revision_request"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
