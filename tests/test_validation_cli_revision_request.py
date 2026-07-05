import json

from constraintos.validation_cli import main

RENDER_SPECIFICATION = "examples/render/lf4_engine_render_specification.yaml"
PASSING_EVIDENCE = "examples/validation/lf4_passing_evidence.yaml"


def test_validation_cli_accepts_revision_request_id(capsys) -> None:
    exit_code = main([
        RENDER_SPECIFICATION,
        "--evidence",
        PASSING_EVIDENCE,
        "--revision-request-id",
        "REVISION-REQUEST-0007",
    ])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["revision_request"]["revision_request"]["id"] == "REVISION-REQUEST-0007"


def test_validation_cli_text_output_includes_revision_request_count(capsys) -> None:
    exit_code = main([RENDER_SPECIFICATION, "--format", "text"])

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "Revision request REVISION-REQUEST-0001: revision_required | steps=3" in output
