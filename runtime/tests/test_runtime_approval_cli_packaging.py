from pathlib import Path


def _pyproject_text() -> str:
    return Path("pyproject.toml").read_text(encoding="utf-8")


def test_runtime_approval_cli_console_script_is_registered() -> None:
    pyproject = _pyproject_text()

    assert 'cos-runtime-approval = "runtime.approval_cli:main"' in pyproject


def test_runtime_release_console_scripts_are_registered() -> None:
    pyproject = _pyproject_text()

    assert 'cos-runtime = "constraintos.runtime_cli:main"' in pyproject
    assert 'cos-runtime-evidence = "runtime.cli:main"' in pyproject
    assert 'cos-runtime-approval = "runtime.approval_cli:main"' in pyproject


def test_runtime_package_discovery_metadata_is_registered() -> None:
    pyproject = _pyproject_text()

    assert 'where = ["src", "."]' in pyproject
    assert 'include = ["constraintos*", "runtime*"]' in pyproject
    assert 'exclude = ["tests*", "runtime.tests*"]' in pyproject
