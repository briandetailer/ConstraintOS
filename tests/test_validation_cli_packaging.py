import tomllib
from pathlib import Path


def test_pyproject_exposes_validation_cli_entry_point() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    scripts = pyproject["project"]["scripts"]

    assert scripts["cos-validate"] == "constraintos.validation_cli:main"
