import io
import json

from runtime.__main__ import run_runtime_cli
from runtime.cli import EVIDENCE_CLI_SUCCESS, EVIDENCE_CLI_USAGE_ERROR


def test_runtime_module_cli_dispatches_evidence_command(tmp_path) -> None:
    spec_path = tmp_path / "spec.json"
    workers_path = tmp_path / "workers.json"
    output_dir = tmp_path / "evidence-output"
    spec_path.write_text(
        json.dumps(
            {
                "artifact": {"id": "SPEC-0001"},
                "execution_steps": [{"id": "NODE-0001", "plugin": "generic", "action": "prepare"}],
            }
        ),
        encoding="utf-8",
    )
    workers_path.write_text(
        json.dumps({"workers": [{"worker_id": "WORKER-0001", "plugins": ["generic"]}]}),
        encoding="utf-8",
    )
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_runtime_cli(
        [
            "evidence",
            "--spec",
            str(spec_path),
            "--workers",
            str(workers_path),
            "--output-dir",
            str(output_dir),
        ],
        stdout=stdout,
        stderr=stderr,
    )

    summary = json.loads(stdout.getvalue())
    assert exit_code == EVIDENCE_CLI_SUCCESS
    assert stderr.getvalue() == ""
    assert summary["runtime_evidence_cli"]["successful"] is True
    assert summary["runtime_evidence_cli"]["runtime_id"] == "RUNTIME-0001"
    assert (output_dir / "evidence" / "RUNTIME-0001.json").exists()


def test_runtime_module_cli_reports_help() -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_runtime_cli(["--help"], stdout=stdout, stderr=stderr)

    assert exit_code == EVIDENCE_CLI_SUCCESS
    assert "Usage: python -m runtime evidence" in stdout.getvalue()
    assert "python -m runtime approval" in stdout.getvalue()
    assert stderr.getvalue() == ""


def test_runtime_module_cli_reports_unknown_command() -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_runtime_cli(["unknown"], stdout=stdout, stderr=stderr)

    assert exit_code == EVIDENCE_CLI_USAGE_ERROR
    assert stdout.getvalue() == ""
    assert "Unknown Runtime command: unknown" in stderr.getvalue()
    assert "Usage: python -m runtime evidence" in stderr.getvalue()
