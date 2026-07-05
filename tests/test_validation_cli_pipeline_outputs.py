import json

from constraintos.validation_cli import main

RENDER_SPECIFICATION = "examples/render/lf4_engine_render_specification.yaml"
PASSING_EVIDENCE = "examples/validation/lf4_passing_evidence.yaml"


def test_validation_cli_accepts_pipeline_output_ids(capsys) -> None:
    exit_code = main([
        RENDER_SPECIFICATION,
        "--evidence",
        PASSING_EVIDENCE,
        "--failure-report-id",
        "FAILURE-REPORT-0007",
        "--remediation-plan-id",
        "REMEDIATION-PLAN-0007",
    ])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["failure_report"]["failure_report"]["id"] == "FAILURE-REPORT-0007"
    assert payload["remediation_plan"]["remediation_plan"]["id"] == "REMEDIATION-PLAN-0007"


def test_validation_cli_text_output_includes_failure_and_remediation_counts(capsys) -> None:
    exit_code = main([RENDER_SPECIFICATION, "--format", "text"])

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "Failure report FAILURE-REPORT-0001: failed | failures=3" in output
    assert "Remediation plan REMEDIATION-PLAN-0001: required | actions=3" in output
