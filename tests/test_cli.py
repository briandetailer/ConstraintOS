from pathlib import Path

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


def test_invalid_id(tmp_path: Path) -> None:
    output = tmp_path / "bad.yaml"
    rc = main(["new-artifact", "BAD", "Bad Artifact", "--output", str(output)])
    assert rc == 2
    assert not output.exists()
