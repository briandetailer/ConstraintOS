import io
import json
from pathlib import Path

from runtime import ArtifactStore, RuntimeEngine, RuntimeEvidenceBundleWriter
from runtime.__main__ import run_runtime_cli
from runtime.approval_cli import APPROVAL_CLI_SUCCESS
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


def _evidence_manifest_artifact(tmp_path: Path) -> dict:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [{"id": "NODE-0001", "plugin": "generic", "action": "prepare"}],
    }
    result = RuntimeEngine().run(specification, [WorkerCapability("WORKER-0001", ["generic"])])
    artifact = RuntimeEvidenceBundleWriter(ArtifactStore(tmp_path / "evidence-input")).write_evidence(result.to_dict())
    return artifact.to_dict()


def test_runtime_module_cli_dispatches_approval_command(tmp_path) -> None:
    manifest_artifact = _evidence_manifest_artifact(tmp_path)
    policy_path = tmp_path / "policy.json"
    output_dir = tmp_path / "approval-output"
    policy_path.write_text(json.dumps(_approval_policy()), encoding="utf-8")
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_runtime_cli(
        [
            "approval",
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
    assert summary["runtime_approval_cli"]["successful"] is True
    assert summary["runtime_approval_cli"]["runtime_id"] == "RUNTIME-0001"
    assert (output_dir / "approvals" / "RUNTIME-0001.json").exists()
