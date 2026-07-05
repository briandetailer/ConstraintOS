import tomllib
from pathlib import Path


def test_pyproject_packages_runtime_module() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    package_finder = pyproject["tool"]["setuptools"]["packages"]["find"]

    assert "src" in package_finder["where"]
    assert "." in package_finder["where"]
    assert "constraintos*" in package_finder["include"]
    assert "runtime*" in package_finder["include"]
    assert "runtime.tests*" in package_finder["exclude"]


def test_pyproject_exposes_runtime_cli_entry_point() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    scripts = pyproject["project"]["scripts"]

    assert scripts["cos-runtime"] == "constraintos.runtime_cli:main"
