import json
from copy import deepcopy
from pathlib import Path

from runtime import (
    ArtifactStore,
    RuntimeEngine,
    RuntimeEvidenceBundleWriter,
    create_runtime_approval_decision,
    verify_runtime_approval_decision,
)
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
    artifact = RuntimeEvidenceBundleWriter(ArtifactStore(tmp_path)).write_evidence(_completed_runtime_result())
    return artifact.to_dict()


def test_evidence_linked_runtime_approval_helper_approves_valid_evidence_and_policy(tmp_path) -> None:
    decision = create_runtime_approval_decision(
        _evidence_manifest_artifact(tmp_path),
        _approval_policy(),
        decided_by="policy-owner",
        decided_at="2026-07-06T00:00:00Z",
    )

    assert decision["runtime_approval"] == {
        "runtime_id": "RUNTIME-0001",
        "evidence_manifest_artifact_id": "ARTIFACT-0004",
        "decision": "approved",
        "decided_by": "policy-owner",
        "decided_at": "2026-07-06T00:00:00Z",
        "approval_policy": "default-runtime-approval/v1",
    }
    assert [check["status"] for check in decision["checks"]] == ["passed", "passed"]
    assert decision["notes"] == []
    assert verify_runtime_approval_decision(decision).successful()


def test_evidence_linked_runtime_approval_helper_rejects_invalid_evidence(tmp_path) -> None:
    manifest_artifact = _evidence_manifest_artifact(tmp_path)
    manifest_path = Path(manifest_artifact["metadata"]["path"])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["artifacts"] = [manifest["artifacts"][1], manifest["artifacts"][0], manifest["artifacts"][2]]
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    decision = create_runtime_approval_decision(
        manifest_artifact,
        _approval_policy(),
        decided_by="policy-owner",
        decided_at="2026-07-06T00:00:00Z",
    )

    assert decision["runtime_approval"]["decision"] == "rejected"
    assert [check["status"] for check in decision["checks"]] == ["failed", "passed"]
    assert (
        "Runtime evidence artifacts must include runtime_report, runtime_trace_report, then runtime_contract_registry."
        in decision["notes"]
    )
    assert verify_runtime_approval_decision(decision).successful()


def test_evidence_linked_runtime_approval_helper_does_not_mutate_inputs(tmp_path) -> None:
    manifest_artifact = _evidence_manifest_artifact(tmp_path)
    policy = _approval_policy()
    original_manifest_artifact = deepcopy(manifest_artifact)
    original_policy = deepcopy(policy)

    create_runtime_approval_decision(
        manifest_artifact,
        policy,
        decided_by="policy-owner",
        decided_at="2026-07-06T00:00:00Z",
    )

    assert manifest_artifact == original_manifest_artifact
    assert policy == original_policy
