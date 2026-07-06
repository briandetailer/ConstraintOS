import json

from constraintos.validation_cli import apply_constraint_pack_files, main

RENDER_SPECIFICATION = "examples/render/lf4_engine_render_specification.yaml"
CONSTRAINT_PACK = "examples/constraint_packs/lf4_engine_constraint_pack.yaml"
PASSING_EVIDENCE = "examples/validation/lf4_passing_evidence.yaml"


def test_validation_cli_accepts_constraint_pack(capsys) -> None:
    exit_code = main([
        RENDER_SPECIFICATION,
        "--constraint-pack",
        CONSTRAINT_PACK,
        "--evidence",
        PASSING_EVIDENCE,
    ])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["validation"]["validation_report"]["status"] == "passed"
    assert payload["approval"]["approval"]["status"] == "approved"


def test_validation_cli_accepts_multiple_constraint_packs_without_duplicates(capsys) -> None:
    exit_code = main([
        RENDER_SPECIFICATION,
        "--constraint-pack",
        CONSTRAINT_PACK,
        "--constraint-pack",
        CONSTRAINT_PACK,
        "--format",
        "text",
    ])

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "Validation VALIDATION-REPORT-0001: failed | results=3" in output


def test_apply_constraint_pack_files_applies_packs_before_validation() -> None:
    render_specification = {
        "render_specification": {"id": "RSPEC-9999", "title": "Minimal", "status": "draft", "version": "0.1"},
        "subject": {"id": "SUBJECT-0001", "name": "Subject", "type": "engine"},
        "requirements": [],
        "validation": {"gates": []},
    }

    applied = apply_constraint_pack_files(render_specification, [CONSTRAINT_PACK])

    assert [item["id"] for item in applied["requirements"]] == ["REQ-0001", "REQ-0002", "REQ-0003"]
    assert [item["id"] for item in applied["validation"]["gates"]] == ["GATE-0001", "GATE-0002", "GATE-0003"]
