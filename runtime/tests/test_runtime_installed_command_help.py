import json

import pytest

from constraintos.runtime_cli import main as runtime_main
from runtime.approval_cli import main as approval_main
from runtime.cli import main as evidence_main


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


def _generate_evidence_with_installed_command(tmp_path, capsys):
    spec_path = _write_runtime_specification(tmp_path)
    workers_path = _write_workers(tmp_path)
    output_dir = tmp_path / "evidence-output"

    with pytest.raises(SystemExit) as exc_info:
        evidence_main(
            [
                "--spec",
                str(spec_path),
                "--workers",
                str(workers_path),
                "--output-dir",
                str(output_dir),
            ]
        )

    captured = capsys.readouterr()
    assert exc_info.value.code == 0
    assert captured.err == ""
    return output_dir, json.loads(captured.out)


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


def test_runtime_evidence_installed_command_generates_evidence_package(tmp_path, capsys) -> None:
    output_dir, summary = _generate_evidence_with_installed_command(tmp_path, capsys)

    assert summary["runtime_evidence_cli"]["successful"] is True
    assert summary["runtime_evidence_cli"]["runtime_id"] == "RUNTIME-0001"
    assert (output_dir / "reports" / "RUNTIME-0001.json").exists()
    assert (output_dir / "traces" / "RUNTIME-0001.json").exists()
    assert (output_dir / "contracts" / "runtime-contract-registry.json").exists()
    assert (output_dir / "evidence" / "RUNTIME-0001.json").exists()


def test_runtime_approval_installed_command_generates_approval_report(tmp_path, capsys) -> None:
    evidence_output_dir, _summary = _generate_evidence_with_installed_command(tmp_path, capsys)
    manifest_path = evidence_output_dir / "evidence" / "RUNTIME-0001.json"
    policy_path = _write_approval_policy(tmp_path)
    approval_output_dir = tmp_path / "approval-output"

    with pytest.raises(SystemExit) as exc_info:
        approval_main(
            [
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
            ]
        )

    captured = capsys.readouterr()
    approval_summary = json.loads(captured.out)
    assert exc_info.value.code == 0
    assert captured.err == ""
    assert approval_summary["runtime_approval_cli"]["successful"] is True
    assert approval_summary["runtime_approval_cli"]["decision"] == "approved"
    assert approval_summary["runtime_approval_cli"]["runtime_id"] == "RUNTIME-0001"
    assert (approval_output_dir / "approvals" / "RUNTIME-0001.json").exists()
