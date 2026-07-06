import json
from pathlib import Path

import yaml

from constraintos.constraint_pack_cli import apply_constraint_packs, main

RENDER_SPECIFICATION = "examples/render/lf4_engine_render_specification.yaml"
CONSTRAINT_PACK = "examples/constraint_packs/lf4_engine_constraint_pack.yaml"
CONSTRAINT_PACK_REFERENCE = {"id": "CPACK-0001", "version": "0.1", "title": "LF4 Engineering Atlas Constraint Pack"}


def load_yaml(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def write_yaml(path: Path, payload: dict) -> None:
    path.write_text(yaml.safe_dump(payload), encoding="utf-8")


def test_constraint_pack_cli_writes_yaml_output(tmp_path, capsys) -> None:
    output = tmp_path / "applied-render-specification.yaml"

    exit_code = main([RENDER_SPECIFICATION, CONSTRAINT_PACK, "--output", str(output)])

    payload = yaml.safe_load(output.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert "Wrote render specification" in capsys.readouterr().out
    assert payload["constraint_packs"][0]["id"] == "CPACK-0001"


def test_constraint_pack_cli_yaml_output_preserves_traceability_and_gate_ids(tmp_path) -> None:
    output = tmp_path / "applied-render-specification.yaml"

    exit_code = main([RENDER_SPECIFICATION, CONSTRAINT_PACK, "--output", str(output)])

    payload = yaml.safe_load(output.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert payload["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
    assert [item["id"] for item in payload["validation"]["gates"]] == ["GATE-0001", "GATE-0002", "GATE-0003"]


def test_constraint_pack_cli_prints_json_output(capsys) -> None:
    exit_code = main([RENDER_SPECIFICATION, CONSTRAINT_PACK, "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["constraint_packs"][0]["id"] == "CPACK-0001"
    assert [item["id"] for item in payload["validation"]["gates"]] == ["GATE-0001", "GATE-0002", "GATE-0003"]


def test_constraint_pack_cli_json_output_preserves_full_pack_reference(capsys) -> None:
    exit_code = main([RENDER_SPECIFICATION, CONSTRAINT_PACK, "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]


def test_constraint_pack_cli_accepts_multiple_constraint_packs(capsys) -> None:
    exit_code = main([RENDER_SPECIFICATION, CONSTRAINT_PACK, CONSTRAINT_PACK, "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]


def test_constraint_pack_cli_rejects_schema_invalid_render_specification(tmp_path, capsys) -> None:
    invalid_render_specification = tmp_path / "invalid-render-specification.yaml"
    payload = load_yaml(RENDER_SPECIFICATION)
    payload["validation"]["gates"] = []
    write_yaml(invalid_render_specification, payload)

    exit_code = main([str(invalid_render_specification), CONSTRAINT_PACK])

    assert exit_code == 2
    assert "schema:schemas/render-specification.schema.json:validation.gates" in capsys.readouterr().err


def test_constraint_pack_cli_rejects_schema_invalid_constraint_pack(tmp_path, capsys) -> None:
    invalid_pack = tmp_path / "invalid-constraint-pack.yaml"
    payload = load_yaml(CONSTRAINT_PACK)
    payload["validation"]["gates"] = []
    write_yaml(invalid_pack, payload)

    exit_code = main([RENDER_SPECIFICATION, str(invalid_pack)])

    assert exit_code == 2
    assert "schema:schemas/constraint-pack.schema.json:validation.gates" in capsys.readouterr().err


def test_constraint_pack_cli_rejects_constraint_pack_as_render_specification(capsys) -> None:
    exit_code = main([CONSTRAINT_PACK, CONSTRAINT_PACK])

    assert exit_code == 2
    assert "expected render_specification, got constraint_pack" in capsys.readouterr().err


def test_constraint_pack_cli_rejects_render_specification_as_constraint_pack(capsys) -> None:
    exit_code = main([RENDER_SPECIFICATION, RENDER_SPECIFICATION])

    assert exit_code == 2
    assert "expected constraint_pack, got render_specification" in capsys.readouterr().err


def test_apply_constraint_packs_applies_packs_in_order() -> None:
    render_specification = {"render_specification": {"id": "RSPEC-9999"}}
    first_pack = {
        "constraint_pack": {"id": "CPACK-0001", "version": "0.1", "title": "First"},
        "requirements": [{"id": "REQ-0001"}],
        "negative_constraints": [],
        "validation": {"gates": []},
    }
    second_pack = {
        "constraint_pack": {"id": "CPACK-0002", "version": "0.1", "title": "Second"},
        "requirements": [{"id": "REQ-0002"}],
        "negative_constraints": [],
        "validation": {"gates": []},
    }

    applied = apply_constraint_packs(render_specification, [first_pack, second_pack])

    assert [item["id"] for item in applied["constraint_packs"]] == ["CPACK-0001", "CPACK-0002"]
    assert [item["id"] for item in applied["requirements"]] == ["REQ-0001", "REQ-0002"]


def test_constraint_pack_cli_returns_error_for_missing_file(capsys) -> None:
    exit_code = main(["missing.yaml", CONSTRAINT_PACK])

    assert exit_code == 2
    assert "ERROR:" in capsys.readouterr().err
