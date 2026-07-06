import json

from constraintos.validation_cli import main

RENDER_SPECIFICATION = "examples/render/lf4_engine_render_specification.yaml"
PASSING_EVIDENCE = "examples/validation/lf4_passing_evidence.yaml"


def test_validation_cli_approves_passing_evidence(capsys) -> None:
    exit_code = main([
        RENDER_SPECIFICATION,
        "--evidence",
        PASSING_EVIDENCE,
        "--artifact-id",
        "ARTIFACT-0001",
    ])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["validation"]["validation_report"]["status"] == "passed"
    assert payload["approval"]["approval"]["status"] == "approved"
    assert payload["provenance_manifest"]["provenance_manifest"]["status"] == "approved"


def test_validation_cli_rejects_missing_evidence(capsys) -> None:
    exit_code = main([RENDER_SPECIFICATION, "--artifact-id", "ARTIFACT-0001"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert payload["validation"]["validation_report"]["status"] == "failed"
    assert payload["approval"]["approval"]["status"] == "rejected"
    assert payload["provenance_manifest"]["provenance_manifest"]["status"] == "rejected"


def test_validation_cli_writes_text_output(tmp_path, capsys) -> None:
    output = tmp_path / "validation-result.txt"
    exit_code = main([
        RENDER_SPECIFICATION,
        "--evidence",
        PASSING_EVIDENCE,
        "--format",
        "text",
        "--output",
        str(output),
    ])

    assert exit_code == 0
    assert "Wrote validation approval result" in capsys.readouterr().out
    text = output.read_text(encoding="utf-8")
    assert "Validation VALIDATION-REPORT-0001: passed" in text
    assert "Provenance manifest PROVENANCE-0001: approved" in text
