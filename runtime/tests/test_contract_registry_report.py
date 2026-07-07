import json

from runtime import (
    RuntimeContractRegistryReportWriter,
    runtime_contract_registry,
    verify_runtime_contract_registry,
    verify_runtime_contract_registry_report,
)
from runtime.artifacts import ArtifactStore


EXPECTED_RUNTIME_CONTRACT_NAMES = [
    "runtime_result",
    "runtime_report",
    "runtime_traceability",
    "runtime_trace_report",
    "runtime_evidence_manifest",
    "runtime_contract_registry",
    "runtime_approval_decision",
    "runtime_approval_policy",
    "runtime_approval_report",
]


def test_runtime_contract_registry_report_writer_persists_contract_registry(tmp_path) -> None:
    writer = RuntimeContractRegistryReportWriter(ArtifactStore(tmp_path))

    artifact = writer.write_registry()
    registry_path = tmp_path / "contracts" / "runtime-contract-registry.json"
    registry_data = json.loads(registry_path.read_text(encoding="utf-8"))

    assert artifact.producer == "runtime-contracts/v1"
    assert artifact.metadata["artifact_role"] == "runtime_contract_registry"
    assert artifact.metadata["content_type"] == "application/json"
    assert artifact.metadata["registry_version"] == "runtime-contracts/v1"
    assert artifact.metadata["contract_count"] == len(EXPECTED_RUNTIME_CONTRACT_NAMES)
    assert artifact.metadata["path"] == str(registry_path.resolve())
    assert registry_data == runtime_contract_registry()
    assert verify_runtime_contract_registry(registry_data).successful() is True


def test_runtime_contract_registry_report_writer_uses_custom_path(tmp_path) -> None:
    writer = RuntimeContractRegistryReportWriter(ArtifactStore(tmp_path))

    artifact = writer.write_registry(relative_path="public/runtime-contracts.json")
    registry_path = tmp_path / "public" / "runtime-contracts.json"
    registry_data = json.loads(registry_path.read_text(encoding="utf-8"))

    assert artifact.uri == registry_path.resolve().as_uri()
    assert artifact.metadata["registry_version"] == "runtime-contracts/v1"
    assert [contract["name"] for contract in registry_data["contracts"]] == EXPECTED_RUNTIME_CONTRACT_NAMES


def test_runtime_contract_registry_report_verifier_accepts_written_artifact(tmp_path) -> None:
    artifact = RuntimeContractRegistryReportWriter(ArtifactStore(tmp_path)).write_registry()

    verification = verify_runtime_contract_registry_report(artifact)

    assert verification.successful() is True
    assert verification.to_dict() == {
        "runtime_contract_verification": {"successful": True, "issue_count": 0},
        "issues": [],
    }


def test_runtime_contract_registry_report_verifier_reports_metadata_mismatches(tmp_path) -> None:
    artifact = RuntimeContractRegistryReportWriter(ArtifactStore(tmp_path)).write_registry()
    artifact_data = artifact.to_dict()
    artifact_data["metadata"]["artifact_role"] = "wrong_role"
    artifact_data["metadata"]["content_type"] = "text/plain"
    artifact_data["metadata"]["registry_version"] = "wrong-version"
    artifact_data["metadata"]["contract_count"] = 99

    verification = verify_runtime_contract_registry_report(artifact_data)

    assert verification.successful() is False
    assert verification.issues == [
        "Runtime contract registry report artifact_role must be runtime_contract_registry.",
        "Runtime contract registry report content_type must be application/json.",
        "Runtime contract registry report registry_version must match registry version.",
        "Runtime contract registry report contract_count must match registry contract_count.",
    ]
