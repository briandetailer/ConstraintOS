import pytest

from constraintos.runtime_cli import main as runtime_main
from runtime.approval_cli import main as approval_main
from runtime.cli import main as evidence_main


@pytest.mark.parametrize(
    ("command_main", "expected_help_text"),
    [
        (runtime_main, "usage: cos-runtime"),
        (evidence_main, "Generate a Runtime evidence package."),
        (approval_main, "Create a Runtime approval report from evidence and policy."),
    ],
)
def test_runtime_installed_command_help_exits_successfully(command_main, expected_help_text, capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        command_main(["--help"])

    captured = capsys.readouterr()
    assert exc_info.value.code == 0
    assert expected_help_text in captured.out
    assert captured.err == ""
