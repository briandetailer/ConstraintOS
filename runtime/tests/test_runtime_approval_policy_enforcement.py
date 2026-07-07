from pathlib import Path

from runtime import (
    ArtifactStore,
    RuntimeEngine,
    RuntimeEvidenceBundleWriter,
    create_runtime_approval_decision,
    verify_runtime_approval_decision,
    verify_runtime_approval_decision_against_policy,
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
        "required_checks": ["verify_runtime_evidence_manifest", "verify_runtime_approval_policy"],
        "allowed_decisions": ["approved", "rejected", "needs_review", "waived"],
        "allowed_check_statuses": ["passed", "failed", "waived", "needs_review"],
        "approvers": ["policy-owner"],
        "waiver_rules": {"requires_note_or_waived_check": True},
        "rejection_rules": {"requires_note_or_failed_check": True},
    }


def _approval_decision() -> dict:
    return {
        "runtime_approval": {
            "runtime_id": "RUNTIME-0001",
            "evidence_manifest_artifact_id": "ARTIFACT-0004",
            "decision": "approved",
            "decided_by": "policy-owner",
            "decided_at": "2026-07-06T00:00:00Z",
            "approval_policy": "default-runtime-approval/v1",
        },
        "checks": [
            {
                "id": "APPROVAL-CHECK-0001",
                "name": "runtime evidence manifest verified",
                "status": "passed",
                "source": "verify_runtime_evidence_manifest",
            },
            {
                "id": "APPROVAL-CHECK-0002",
                "name": "runtime approval policy verified",
                "status": "passed",
                "source": "verify_runtime_approval_policy",
            },
        ],
        "notes": [],
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


def test_runtime_approval_decision_satisfies_matching_policy() -> None:
    verification = verify_runtime_approval_decision_against_policy(_approval_decision(), _approval_policy())

    assert verification.successful()


def test_runtime_approval_decision_policy_enforcement_rejects_unauthorized_approver() -> None:
    decision = _approval_decision()
    decision["runtime_approval"]["decided_by"] = "unknown-approver"

    verification = verify_runtime_approval_decision_against_policy(decision, _approval_policy())

    assert not verification.successful()
    assert "Runtime approval decision decided_by must be an authorized policy approver." in verification.issues


def test_runtime_approval_decision_policy_enforcement_rejects_missing_required_check() -> None:
    policy = _approval_policy()
    policy["required_checks"].append("human_review_required")

    verification = verify_runtime_approval_decision_against_policy(_approval_decision(), policy)

    assert not verification.successful()
    assert "Runtime approval decision must include all required policy checks." in verification.issues


def test_runtime_approval_decision_policy_enforcement_rejects_policy_name_mismatch() -> None:
    decision = _approval_decision()
    decision["runtime_approval"]["approval_policy"] = "other-policy/v1"

    verification = verify_runtime_approval_decision_against_policy(decision, _approval_policy())

    assert not verification.successful()
    assert "Runtime approval decision approval_policy must match approval policy name." in verification.issues


def test_evidence_linked_runtime_approval_rejects_when_policy_required_check_is_missing(tmp_path) -> None:
    policy = _approval_policy()
    policy["required_checks"].append("human_review_required")

    decision = create_runtime_approval_decision(
        _evidence_manifest_artifact(tmp_path),
        policy,
        decided_by="policy-owner",
        decided_at="2026-07-06T00:00:00Z",
    )

    assert decision["runtime_approval"]["decision"] == "rejected"
    assert [check["status"] for check in decision["checks"]] == ["passed", "passed", "failed"]
    assert "Runtime approval decision must include all required policy checks." in decision["notes"]
    assert verify_runtime_approval_decision(decision).successful()
