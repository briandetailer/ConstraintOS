import io
import json

from runtime.cli import (
    EVIDENCE_CLI_RUNTIME_UNSUCCESSFUL,
    EVIDENCE_CLI_SUCCESS,
    EVIDENCE_CLI_USAGE_ERROR,
    run_evidence_cli,
)


def test_runtime_evidence_cli_generates_and_verifies_evidence_package(tmp_path) -> None:
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

    exit_code = run_evidence_cli(
        [
            "--spec",
            str(spec_path),
            "--workers",
            str(workers_path),
            "--output-dir",
            str(output_dir),
            "--format",
            "json",
        ],
        stdout=stdout,
        stderr=stderr,
    )

    summary = json.loads(stdout.getvalue())
    assert exit_code == EVIDENCE_CLI_SUCCESS
    assert stderr.getvalue() == ""
    assert summary == {
        "runtime_evidence_cli": {
            "successful": True,
            "runtime_id": "RUNTIME-0001",
            "runtime_status": "completed",
            "evidence_manifest_uri": (output_dir / "evidence" / "RUNTIME-0001.json").resolve().as_uri(),
            "evidence_manifest_path": str((output_dir / "evidence" / "RUNTIME-0001.json").resolve()),
            "contract_registry_version": "runtime-contracts/v1",
            "issue_count": 0,
        },
        "issues": [],
    }
    assert (output_dir / "reports" / "RUNTIME-0001.json").exists()
    assert (output_dir / "traces" / "RUNTIME-0001.json").exists()
    assert (output_dir / "contracts" / "runtime-contract-registry.json").exists()
    assert (output_dir / "evidence" / "RUNTIME-0001.json").exists()


def test_runtime_evidence_cli_returns_unsuccessful_when_runtime_is_not_successful(tmp_path) -> None:
    spec_path = tmp_path / "spec.json"
    workers_path = tmp_path / "workers.json"
    output_dir = tmp_path / "evidence-output"
    spec_path.write_text(
        json.dumps(
            {
                "artifact": {"id": "SPEC-0001"},
                "execution_steps": [{"id": "NODE-0001", "plugin": "blender", "action": "render"}],
            }
        ),
        encoding="utf-8",
    )
    workers_path.write_text(
        json.dumps({"workers": [{"worker_id": "WORKER-0001", "plugins": ["generic"]}]}),
        encoding="utf-8",
    )
    stdout = io.StringIO()

    exit_code = run_evidence_cli(
        [
            "--spec",
            str(spec_path),
            "--workers",
            str(workers_path),
            "--output-dir",
            str(output_dir),
        ],
        stdout=stdout,
    )

    summary = json.loads(stdout.getvalue())
    assert exit_code == EVIDENCE_CLI_RUNTIME_UNSUCCESSFUL
    assert summary["runtime_evidence_cli"]["successful"] is False
    assert summary["runtime_evidence_cli"]["runtime_status"] == "partial"
    assert summary["runtime_evidence_cli"]["issue_count"] == 0
    assert (output_dir / "evidence" / "RUNTIME-0001.json").exists()


def test_runtime_evidence_cli_reports_usage_error_for_malformed_workers(tmp_path) -> None:
    spec_path = tmp_path / "spec.json"
    workers_path = tmp_path / "workers.json"
    spec_path.write_text(json.dumps({"artifact": {"id": "SPEC-0001"}, "execution_steps": []}), encoding="utf-8")
    workers_path.write_text(json.dumps({"workers": [{"worker_id": "WORKER-0001", "plugins": "generic"}]}), encoding="utf-8")
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_evidence_cli(
        [
            "--spec",
            str(spec_path),
            "--workers",
            str(workers_path),
            "--output-dir",
            str(tmp_path / "evidence-output"),
        ],
        stdout=stdout,
        stderr=stderr,
    )

    assert exit_code == EVIDENCE_CLI_USAGE_ERROR
    assert stdout.getvalue() == ""
    assert "Worker 1 requires plugins as a list of strings." in stderr.getvalue()
}
