from pathlib import Path

import yaml

from constraintos.cli import main

RENDER_SPECIFICATION = "examples/render/lf4_engine_render_specification.yaml"
CONSTRAINT_PACK = "examples/constraint_packs/lf4_engine_constraint_pack.yaml"
PASSING_EVIDENCE = "examples/validation/lf4_passing_evidence.yaml"


def test_new_artifact(tmp_path: Path) -> None:
    output = tmp_path / "artifact.yaml"
    rc = main(["new-artifact", "CPE-0007", "Test Artifact", "--output", str(output)])
    assert rc == 0
    assert output.exists()
    assert "CPE-0007" in output.read_text()


def test_new_failure(tmp_path: Path) -> None:
    output = tmp_path / "failure.yaml"
    rc = main(["new-failure", "FR-0036", "Test Failure", "--output", str(output)])
    assert rc == 0
    assert output.exists()
    assert "FR-0036" in output.read_text()


def test_new_compliance(tmp_path: Path) -> None:
    output = tmp_path / "VAL-0001.yaml"
    rc = main(["new-compliance", "VAL-0001", "PLATE-0001", "SPEC-0001", "--output", str(output)])
    assert rc == 0
    data = yaml.safe_load(output.read_text())
    assert data["report"]["id"] == "VAL-0001"


def test_registry_generation(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.yaml"
    registry = tmp_path / "registry.yaml"
    main(["new-artifact", "CPE-0007", "Test Artifact", "--output", str(artifact)])
    rc = main(["registry", str(tmp_path), "--output", str(registry)])
    assert rc == 0
    data = yaml.safe_load(registry.read_text())
    assert data["registry"][0]["id"] == "CPE-0007"


def test_export_markdown(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.yaml"
    markdown = tmp_path / "artifact.md"
    main(["new-artifact", "CPE-0007", "Test Artifact", "--output", str(artifact)])
    rc = main(["export-md", str(artifact), "--output", str(markdown)])
    assert rc == 0
    assert "# Test Artifact" in markdown.read_text()


def test_invalid_id(tmp_path: Path) -> None:
    output = tmp_path / "bad.yaml"
    rc = main(["new-artifact", "BAD", "Bad Artifact", "--output", str(output)])
    assert rc == 2
    assert not output.exists()


def test_validate_accepts_registered_render_specification(capsys) -> None:
    rc = main(["validate", RENDER_SPECIFICATION, "--repo-root", "."])

    assert rc == 0
    assert "PASS:" in capsys.readouterr().out


def test_validate_accepts_registered_validation_evidence(capsys) -> None:
    rc = main(["validate", PASSING_EVIDENCE, "--repo-root", "."])

    assert rc == 0
    assert "PASS:" in capsys.readouterr().out


def test_validate_rejects_schema_invalid_render_specification(tmp_path: Path, capsys) -> None:
    invalid_render_specification = tmp_path / "invalid-render-specification.yaml"
    payload = yaml.safe_load(Path(RENDER_SPECIFICATION).read_text(encoding="utf-8"))
    payload["validation"]["gates"] = []
    invalid_render_specification.write_text(yaml.safe_dump(payload), encoding="utf-8")

    rc = main(["validate", str(invalid_render_specification), "--repo-root", "."])

    assert rc == 1
    assert "schema:schemas/render-specification.schema.json:validation.gates" in capsys.readouterr().out


def test_validate_rejects_schema_invalid_constraint_pack(tmp_path: Path, capsys) -> None:
    invalid_constraint_pack = tmp_path / "invalid-constraint-pack.yaml"
    payload = yaml.safe_load(Path(CONSTRAINT_PACK).read_text(encoding="utf-8"))
    payload["validation"]["gates"] = []
    invalid_constraint_pack.write_text(yaml.safe_dump(payload), encoding="utf-8")

    rc = main(["validate", str(invalid_constraint_pack), "--repo-root", "."])

    assert rc == 1
    assert "schema:schemas/constraint-pack.schema.json:validation.gates" in capsys.readouterr().out


def test_validate_rejects_schema_invalid_validation_evidence(tmp_path: Path, capsys) -> None:
    invalid_evidence = tmp_path / "invalid-evidence.yaml"
    invalid_evidence.write_text(yaml.safe_dump({"evidence": [{"status": "passed"}]}), encoding="utf-8")

    rc = main(["validate", str(invalid_evidence), "--repo-root", "."])

    assert rc == 1
    assert "schema:schemas/validation-evidence.schema.json:evidence.0" in capsys.readouterr().out
