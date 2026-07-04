from pathlib import Path

import yaml

from constraintos.cli import main


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
