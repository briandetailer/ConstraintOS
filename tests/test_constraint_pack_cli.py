import json

import yaml

from constraintos.constraint_pack_cli import main

RENDER_SPECIFICATION = "examples/render/lf4_engine_render_specification.yaml"
CONSTRAINT_PACK = "examples/constraint_packs/lf4_engine_constraint_pack.yaml"


def test_constraint_pack_cli_writes_yaml_output(tmp_path, capsys) -> None:
    output = tmp_path / "applied-render-specification.yaml"

    exit_code = main([RENDER_SPECIFICATION, CONSTRAINT_PACK, "--output", str(output)])

    payload = yaml.safe_load(output.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert "Wrote render specification" in capsys.readouterr().out
    assert payload["constraint_packs"][0]["id"] == "CPACK-0001"


def test_constraint_pack_cli_prints_json_output(capsys) -> None:
    exit_code = main([RENDER_SPECIFICATION, CONSTRAINT_PACK, "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["constraint_packs"][0]["id"] == "CPACK-0001"
    assert [item["id"] for item in payload["validation"]["gates"]] == ["GATE-0001", "GATE-0002", "GATE-0003"]


def test_constraint_pack_cli_returns_error_for_missing_file(capsys) -> None:
    exit_code = main(["missing.yaml", CONSTRAINT_PACK])

    assert exit_code == 2
    assert "ERROR:" in capsys.readouterr().err
