import io
import json
from pathlib import Path

from runtime import ArtifactStore, RuntimeEngine, RuntimeEvidenceBundleWriter
from runtime.approval_cli import APPROVAL_CLI_REJECTED, APPROVAL_CLI_SUCCESS, APPROVAL_CLI_USAGE_ERROR, run_approval_cli
from runtime.scheduler import WorkerCapability


def _approval_policy() -> dict:
    return {
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


def _completed_runtime_result() -> dict:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [{"id": "NODE-0001", "plugin": "generic", "action": "prepare"}],
    }
    result = RuntimeEngine().run(specification, [WorkerCapability("WORKER-0001", ["generic"])])
    return result.to_dict()


def _evidence_manifest_artifact(tmp_path: Path) -> dict:
    artifact = RuntimeEvidenceBundleWriter(ArtifactStore(tmp_path / "evidence-input")).write_evidence(_completed_runtime_result())
    return artifact.to_dict()


def _write_policy(tmp_path: Path, policy: dict | list) -> Path:
    policy_path = tmp_path / "policy.json"
    policy_path.write_text(json.dumps(policy), encoding="utf-8")
    return policy_path


def test_runtime_approval_cli_generates_approved_report(tmp_path) -> None:
    manifest_artifact = _evidence_manifest_artifact(tmp_path)
    policy_path = _write_policy(tmp_path, _approval_policy())
    output_dir = tmp_path / "approval-output"
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_approval_cli(
        [
            "--evidence-manifest",
            manifest_artifact["metadata"]["path"],
            "--evidence-artifact-id",
            manifest_artifact["id"],
            "--policy",
            str(policy_path),
            "--decided-by",
            "policy-owner",
            "--decided-at",
            "2026-07-06T00:00:00Z",
            "--output-dir",
            str(output_dir),
        ],
        stdout=stdout,
        stderr=stderr,
    )

    summary = json.loads(stdout.getvalue())
    assert exit_code == APPROVAL_CLI_SUCCESS
    assert stderr.getvalue() == ""
    assert summary["runtime_approval_cli"] == {
        "successful": True,
        "runtime_id": "RUNTIME-0001",
        "decision": "approved",
        "approval_policy": "default-runtime-approval/v1",
        "evidence_manifest_artifact_id": "ARTIFACT-0004",
        "approval_report_uri": (output_dir / "approvals" / "RUNTIME-0001.json").resolve().as_uri(),
        "approval_report_path": str((output_dir / "approvals" / "RUNTIME-0001.json").resolve()),
        "issue_count": 0,
    }
    assert [check["status"] for check in summary["checks"]] == ["passed", "passed"]
    assert summary["issues"] == []
    assert (output_dir / "approvals" / "RUNTIME-0001.json").exists()


def test_runtime_approval_cli_returns_rejected_for_invalid_evidence(tmp_path) -> None:
    manifest_artifact = _evidence_manifest_artifact(tmp_path)
    manifest_path = Path(manifest_artifact["metadata"]["path"])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["artifacts"] = [manifest["artifacts"][1], manifest["artifacts"][0], manifest["artifacts"][2]]
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    policy_path = _write_policy(tmp_path, _approval_policy())
    output_dir = tmp_path / "approval-output"
    stdout = io.StringIO()

    exit_code = run_approval_cli(
        [
            "--evidence-manifest",
            manifest_artifact["metadata"]["path"],
            "--evidence-artifact-id",
            manifest_artifact["id"],
            "--policy",
            str(policy_path),
            "--decided-by",
            "policy-owner",
            "--decided-at",
            "2026-07-06T00:00:00Z",
            "--output-dir",
            str(output_dir),
        ],
        stdout=stdout,
    )

    summary = json.loads(stdout.getvalue())
    assert exit_code == APPROVAL_CLI_REJECTED
    assert summary["runtime_approval_cli"]["successful"] is False
    assert summary["runtime_approval_cli"]["decision"] == "rejected"
    assert summary["runtime_approval_cli"]["issue_count"] == len(summary["issues"])
    assert [check["status"] for check in summary["checks"]] == ["failed", "passed"]
    assert (
        "Runtime evidence artifacts must include runtime_report, runtime_trace_report, then runtime_contract_registry."
        in summary["issues"]
    )
    assert (output_dir / "approvals" / "RUNTIME-0001.json").exists()


def test_runtime_approval_cli_reports_usage_error_for_malformed_policy(tmp_path) -> None:
    manifest_artifact = _evidence_manifest_artifact(tmp_path)
    policy_path = _write_policy(tmp_path, [])
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_approval_cli(
        [
            "--evidence-manifest",
            manifest_artifact["metadata"]["path"],
            "--evidence-artifact-id",
            manifest_artifact["id"],
            "--policy",
            str(policy_path),
            "--decided-by",
            "policy-owner",
            "--decided-at",
            "2026-07-06T00:00:00Z",
            "--output-dir",
            str(tmp_path / "approval-output"),
        ],
        stdout=stdout,
        stderr=stderr,
    )

    assert exit_code == APPROVAL_CLI_USAGE_ERROR
    assert stdout.getvalue() == ""
    assert f"{policy_path} must contain a JSON object." in stderr.getvalue()
