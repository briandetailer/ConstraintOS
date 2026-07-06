import json

from runtime import RuntimeContractRegistryReportWriter, runtime_contract_registry, verify_runtime_contract_registry
from runtime.artifacts import ArtifactStore


def test_runtime_contract_registry_report_writer_persists_contract_registry(tmp_path) -> None:
    writer = RuntimeContractRegistryReportWriter(ArtifactStore(tmp_path))

    artifact = writer.write_registry()
    registry_path = tmp_path / "contracts" / "runtime-contract-registry.json"
    registry_data = json.loads(registry_path.read_text(encoding="utf-8"))

    assert artifact.producer == "runtime-contracts/v1"
    assert artifact.metadata["artifact_role"] == "runtime_contract_registry"
    assert artifact.metadata["content_type"] == "application/json"
    assert artifact.metadata["registry_version"] == "runtime-contracts/v1"
    assert artifact.metadata["contract_count"] == 4
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
    assert [contract["name"] for contract in registry_data["contracts"]] == [
        "runtime_result",
        "runtime_traceability",
        "runtime_trace_report",
        "runtime_evidence_manifest",
    ]
