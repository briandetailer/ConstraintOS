from pathlib import Path

import yaml

from constraintos.validation.pipeline import ValidationApprovalPipeline


def load_lf4_specification() -> dict:
    source = Path("examples/render/lf4_engine_render_specification.yaml")
    return yaml.safe_load(source.read_text(encoding="utf-8"))


def test_pipeline_result_includes_not_required_revision_request_when_approved() -> None:
    result = ValidationApprovalPipeline().evaluate_render_specification(
        load_lf4_specification(),
        evidence=[
            {"gate_id": "GATE-0001", "status": "passed"},
            {"gate_id": "GATE-0002", "status": "passed"},
            {"gate_id": "GATE-0003", "status": "passed"},
        ],
        artifact_id="ARTIFACT-0001",
    )

    assert result.revision_request.status == "not_required"
    assert result.revision_request.steps == []
    assert result.to_dict()["revision_request"]["revision_request"]["step_count"] == 0


def test_pipeline_result_includes_revision_request_when_rejected() -> None:
    result = ValidationApprovalPipeline().evaluate_render_specification(
        load_lf4_specification(),
        evidence=[
            {"gate_id": "GATE-0001", "status": "passed"},
            {"gate_id": "GATE-0002", "status": "passed"},
        ],
        artifact_id="ARTIFACT-0001",
        revision_request_id="REVISION-REQUEST-0007",
    )

    step = result.revision_request.steps[0]
    assert result.revision_request.status == "revision_required"
    assert result.revision_request.id == "REVISION-REQUEST-0007"
    assert result.revision_request.artifact_id == "ARTIFACT-0001"
    assert step["gate_id"] == "GATE-0003"
    assert step["issue_code"] == "VAL-0001"
