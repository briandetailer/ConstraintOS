from pathlib import Path

import yaml

from constraintos.validation.pipeline import ValidationApprovalPipeline


def load_lf4_specification() -> dict:
    source = Path("examples/render/lf4_engine_render_specification.yaml")
    return yaml.safe_load(source.read_text(encoding="utf-8"))


def test_pipeline_result_includes_not_required_remediation_plan_when_approved() -> None:
    result = ValidationApprovalPipeline().evaluate_render_specification(
        load_lf4_specification(),
        evidence=[
            {"gate_id": "GATE-0001", "status": "passed"},
            {"gate_id": "GATE-0002", "status": "passed"},
            {"gate_id": "GATE-0003", "status": "passed"},
        ],
    )

    assert result.remediation_plan.status == "not_required"
    assert result.remediation_plan.actions == []
    assert result.to_dict()["remediation_plan"]["remediation_plan"]["action_count"] == 0


def test_pipeline_result_includes_required_remediation_plan_when_rejected() -> None:
    result = ValidationApprovalPipeline().evaluate_render_specification(
        load_lf4_specification(),
        evidence=[
            {"gate_id": "GATE-0001", "status": "passed"},
            {"gate_id": "GATE-0002", "status": "passed"},
        ],
    )

    action = result.remediation_plan.actions[0]
    assert result.remediation_plan.status == "required"
    assert action["gate_id"] == "GATE-0003"
    assert action["issue_code"] == "VAL-0001"
    assert action["instruction"] == "Supply evidence for the required validation gate."
