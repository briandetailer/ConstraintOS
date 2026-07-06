import json
from pathlib import Path

import yaml

from constraintos.validation_cli import apply_constraint_pack_files, main

RENDER_SPECIFICATION = "examples/render/lf4_engine_render_specification.yaml"
CONSTRAINT_PACK = "examples/constraint_packs/lf4_engine_constraint_pack.yaml"
PASSING_EVIDENCE = "examples/validation/lf4_passing_evidence.yaml"
CONSTRAINT_PACK_REFERENCE = {"id": "CPACK-0001", "version": "0.1", "title": "LF4 Engineering Atlas Constraint Pack"}


def load_yaml(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def write_yaml(path: Path, payload: dict) -> None:
    path.write_text(yaml.safe_dump(payload), encoding="utf-8")


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


def test_validation_cli_json_preserves_constraint_pack_traceability(capsys) -> None:
    exit_code = main([
        RENDER_SPECIFICATION,
        "--constraint-pack",
        CONSTRAINT_PACK,
        "--evidence",
        PASSING_EVIDENCE,
    ])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["validation"]["validation_report"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
    assert payload["failure_report"]["failure_report"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
    assert payload["remediation_plan"]["remediation_plan"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
    assert payload["revision_request"]["revision_request"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
    assert payload["approval"]["approval"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]


def test_validation_cli_text_reports_constraint_pack_count(capsys) -> None:
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
    assert "Constraint packs: 1" in output


def test_validation_cli_rejects_schema_invalid_render_specification(tmp_path, capsys) -> None:
    invalid_render_specification = tmp_path / "invalid-render-specification.yaml"
    payload = load_yaml(RENDER_SPECIFICATION)
    payload["validation"]["gates"] = []
    write_yaml(invalid_render_specification, payload)

    exit_code = main([str(invalid_render_specification), "--evidence", PASSING_EVIDENCE])

    assert exit_code == 2
    assert "schema:schemas/render-specification.schema.json:validation.gates" in capsys.readouterr().err


def test_validation_cli_rejects_schema_invalid_constraint_pack(tmp_path, capsys) -> None:
    invalid_pack = tmp_path / "invalid-constraint-pack.yaml"
    payload = load_yaml(CONSTRAINT_PACK)
    payload["validation"]["gates"] = []
    write_yaml(invalid_pack, payload)

    exit_code = main([RENDER_SPECIFICATION, "--constraint-pack", str(invalid_pack)])

    assert exit_code == 2
    assert "schema:schemas/constraint-pack.schema.json:validation.gates" in capsys.readouterr().err


def test_validation_cli_rejects_schema_invalid_evidence(tmp_path, capsys) -> None:
    invalid_evidence = tmp_path / "invalid-evidence.yaml"
    write_yaml(invalid_evidence, {"evidence": [{"status": "passed"}]})

    exit_code = main([RENDER_SPECIFICATION, "--evidence", str(invalid_evidence)])

    assert exit_code == 2
    assert "schema:schemas/validation-evidence.schema.json:evidence.0" in capsys.readouterr().err


def test_validation_cli_rejects_evidence_for_unknown_gate(tmp_path, capsys) -> None:
    evidence = tmp_path / "unknown-gate-evidence.yaml"
    write_yaml(evidence, {"evidence": [{"gate_id": "GATE-9999", "status": "passed"}]})

    exit_code = main([RENDER_SPECIFICATION, "--evidence", str(evidence)])

    assert exit_code == 2
    assert "unknown gate: GATE-9999" in capsys.readouterr().err


def test_validation_cli_rejects_duplicate_gate_evidence(tmp_path, capsys) -> None:
    evidence = tmp_path / "duplicate-gate-evidence.yaml"
    write_yaml(
        evidence,
        {
            "evidence": [
                {"gate_id": "GATE-0001", "status": "passed"},
                {"gate_id": "GATE-0001", "status": "passed"},
            ]
        },
    )

    exit_code = main([RENDER_SPECIFICATION, "--evidence", str(evidence)])

    assert exit_code == 2
    assert "duplicate validation evidence for gate: GATE-0001" in capsys.readouterr().err


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
