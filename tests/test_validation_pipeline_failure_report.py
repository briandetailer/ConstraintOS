from pathlib import Path

import yaml

from constraintos.validation.pipeline import ValidationApprovalPipeline


def load_lf4_specification() -> dict:
    source = Path("examples/render/lf4_engine_render_specification.yaml")
    return yaml.safe_load(source.read_text(encoding="utf-8"))


def test_pipeline_result_includes_empty_failure_report_when_approved() -> None:
    result = ValidationApprovalPipeline().evaluate_render_specification(
        load_lf4_specification(),
        evidence=[
            {"gate_id": "GATE-0001", "status": "passed"},
            {"gate_id": "GATE-0002", "status": "passed"},
            {"gate_id": "GATE-0003", "status": "passed"},
        ],
    )

    assert result.failure_report.status == "passed"
    assert result.failure_report.failures == []
    assert result.to_dict()["failure_report"]["failure_report"]["failure_count"] == 0


def test_pipeline_result_includes_failure_report_when_rejected() -> None:
    result = ValidationApprovalPipeline().evaluate_render_specification(
        load_lf4_specification(),
        evidence=[
            {"gate_id": "GATE-0001", "status": "passed"},
            {"gate_id": "GATE-0002", "status": "passed"},
        ],
    )

    failure = result.failure_report.failures[0]
    assert result.approval_decision.status == "rejected"
    assert result.failure_report.status == "failed"
    assert failure["gate_id"] == "GATE-0003"
    assert failure["issue_code"] == "VAL-0001"
