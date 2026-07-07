import io
import json

from runtime.__main__ import run_runtime_cli
from runtime.cli import EVIDENCE_CLI_SUCCESS, EVIDENCE_CLI_USAGE_ERROR


def _write_runtime_specification(tmp_path):
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(
        json.dumps(
            {
                "artifact": {"id": "SPEC-0001"},
                "execution_steps": [{"id": "NODE-0001", "plugin": "generic", "action": "prepare"}],
            }
        ),
        encoding="utf-8",
    )
    return spec_path


def _write_workers(tmp_path):
    workers_path = tmp_path / "workers.json"
    workers_path.write_text(
        json.dumps({"workers": [{"worker_id": "WORKER-0001", "plugins": ["generic"]}]}),
        encoding="utf-8",
    )
    return workers_path


def _write_approval_policy(tmp_path):
    policy_path = tmp_path / "policy.json"
    policy_path.write_text(
        json.dumps(
            {
                "runtime_approval_policy": {
                    "name": "default-runtime-approval/v1",
                    "version": "v1",
                    "contract_registry_version": "runtime-contracts/v1",
                },
                "required_evidence_artifacts": [
                    "runtime_report",
                    "runtime_trace_report",
                    "runtime_contract_registry",
                    "runtime_evidence_manifest",
                ],
                "required_checks": ["verify_runtime_evidence_manifest"],
                "allowed_decisions": ["approved", "rejected", "needs_review", "waived"],
                "allowed_check_statuses": ["passed", "failed", "waived", "needs_review"],
                "approvers": ["policy-owner"],
                "waiver_rules": {"requires_note_or_waived_check": True},
                "rejection_rules": {"requires_note_or_failed_check": True},
            }
        ),
        encoding="utf-8",
    )
    return policy_path


def _generate_evidence_with_runtime_module(tmp_path):
    spec_path = _write_runtime_specification(tmp_path)
    workers_path = _write_workers(tmp_path)
    output_dir = tmp_path / "evidence-output"
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

    assert exit_code == EVIDENCE_CLI_SUCCESS
    assert stderr.getvalue() == ""
    return output_dir, json.loads(stdout.getvalue())


def test_runtime_module_cli_dispatches_evidence_command(tmp_path) -> None:
    output_dir, summary = _generate_evidence_with_runtime_module(tmp_path)

    assert summary["runtime_evidence_cli"]["successful"] is True
    assert summary["runtime_evidence_cli"]["runtime_id"] == "RUNTIME-0001"
    assert (output_dir / "evidence" / "RUNTIME-0001.json").exists()


def test_runtime_module_cli_dispatches_approval_command(tmp_path) -> None:
    evidence_output_dir, _summary = _generate_evidence_with_runtime_module(tmp_path)
    manifest_path = evidence_output_dir / "evidence" / "RUNTIME-0001.json"
    policy_path = _write_approval_policy(tmp_path)
    approval_output_dir = tmp_path / "approval-output"
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_runtime_cli(
        [
            "approval",
            "--evidence-manifest",
            str(manifest_path),
            "--evidence-artifact-id",
            "ARTIFACT-0004",
            "--policy",
            str(policy_path),
            "--decided-by",
            "policy-owner",
            "--decided-at",
            "2026-07-06T00:00:00Z",
            "--output-dir",
            str(approval_output_dir),
        ],
        stdout=stdout,
        stderr=stderr,
    )

    summary = json.loads(stdout.getvalue())
    assert exit_code == EVIDENCE_CLI_SUCCESS
    assert stderr.getvalue() == ""
    assert summary["runtime_approval_cli"]["successful"] is True
    assert summary["runtime_approval_cli"]["runtime_id"] == "RUNTIME-0001"
    assert summary["runtime_approval_cli"]["decision"] == "approved"
    assert (approval_output_dir / "approvals" / "RUNTIME-0001.json").exists()


def test_runtime_module_cli_reports_help() -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_runtime_cli(["--help"], stdout=stdout, stderr=stderr)

    assert exit_code == EVIDENCE_CLI_SUCCESS
    assert "Usage: python -m runtime evidence" in stdout.getvalue()
    assert "python -m runtime approval" in stdout.getvalue()
    assert stderr.getvalue() == ""


def test_runtime_module_cli_reports_missing_command() -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_runtime_cli([], stdout=stdout, stderr=stderr)

    assert exit_code == EVIDENCE_CLI_USAGE_ERROR
    assert stdout.getvalue() == ""
    assert "Usage: python -m runtime evidence" in stderr.getvalue()


def test_runtime_module_cli_reports_unknown_command() -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_runtime_cli(["unknown"], stdout=stdout, stderr=stderr)

    assert exit_code == EVIDENCE_CLI_USAGE_ERROR
    assert stdout.getvalue() == ""
    assert "Unknown Runtime command: unknown" in stderr.getvalue()
    assert "Usage: python -m runtime evidence" in stderr.getvalue()
