from pathlib import Path


def test_runtime_approval_cli_console_script_is_registered() -> None:
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")

    assert 'cos-runtime-approval = "runtime.approval_cli:main"' in pyproject
