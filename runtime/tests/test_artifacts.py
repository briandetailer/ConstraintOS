import pytest

from runtime.artifacts import ArtifactCollector, ArtifactStore, ArtifactStoreError, RuntimeArtifact
from runtime.execution import ExecutionResult, NodeExecutionResult


def test_runtime_artifact_serializes_metadata() -> None:
    artifact = RuntimeArtifact(
        id="ARTIFACT-0001",
        uri="file:///tmp/output.txt",
        kind="file",
        producer="NODE-0001",
        metadata={"content_type": "text/plain"},
    )

    assert artifact.to_dict() == {
        "id": "ARTIFACT-0001",
        "uri": "file:///tmp/output.txt",
        "kind": "file",
        "producer": "NODE-0001",
        "metadata": {"content_type": "text/plain"},
    }


def test_artifact_store_registers_and_lists_artifacts() -> None:
    store = ArtifactStore()
    artifact = store.register(RuntimeArtifact("ARTIFACT-0001", "memory://artifact-1", producer="NODE-0001"))

    assert artifact.id == "ARTIFACT-0001"
    assert store.get("ARTIFACT-0001") == artifact
    assert store.list() == [artifact]
    assert store.to_dict()["artifact_store"]["count"] == 1


def test_artifact_store_generates_sequential_artifact_ids() -> None:
    store = ArtifactStore()

    first = store.record_uri("memory://first")
    second = store.record_uri("memory://second")

    assert first.id == "ARTIFACT-0001"
    assert second.id == "ARTIFACT-0002"


def test_artifact_store_rejects_duplicate_artifact_ids() -> None:
    store = ArtifactStore()
    store.record_uri("memory://first", artifact_id="ARTIFACT-0001")

    with pytest.raises(ArtifactStoreError, match="Artifact ARTIFACT-0001 is already registered"):
        store.record_uri("memory://duplicate", artifact_id="ARTIFACT-0001")


def test_artifact_store_writes_text_artifact(tmp_path) -> None:
    store = ArtifactStore(tmp_path)

    artifact = store.write_text(
        "reports/result.txt",
        "runtime complete",
        artifact_id="ARTIFACT-0001",
        producer="NODE-0001",
        metadata={"content_type": "text/plain"},
    )

    written = tmp_path / "reports" / "result.txt"
    assert written.read_text(encoding="utf-8") == "runtime complete"
    assert artifact.uri == written.resolve().as_uri()
    assert artifact.metadata["path"] == str(written.resolve())
    assert artifact.metadata["content_type"] == "text/plain"


def test_artifact_store_rejects_paths_that_escape_root(tmp_path) -> None:
    store = ArtifactStore(tmp_path)

    with pytest.raises(ArtifactStoreError, match="artifact path cannot escape"):
        store.write_text("../outside.txt", "nope")


def test_artifact_collector_records_execution_outputs() -> None:
    execution = ExecutionResult(
        id="EXEC-RESULT-0001",
        request_id="EXEC-REQ-0001",
        status="complete",
        node_results=[
            NodeExecutionResult(
                node_id="NODE-0001",
                worker_id="WORKER-0001",
                plugin="echo",
                action="package",
                status="complete",
                outputs=["echo://NODE-0001"],
            )
        ],
    )
    store = ArtifactStore()
    collector = ArtifactCollector(store)

    artifacts = collector.collect_from_execution(execution)

    assert len(artifacts) == 1
    assert artifacts[0].id == "ARTIFACT-0001"
    assert artifacts[0].uri == "echo://NODE-0001"
    assert artifacts[0].producer == "NODE-0001"
    assert artifacts[0].metadata["worker_id"] == "WORKER-0001"
    assert artifacts[0].metadata["plugin"] == "echo"
    assert store.to_dict()["artifact_store"]["count"] == 1


def test_artifact_collector_ignores_empty_or_non_string_outputs() -> None:
    execution = {
        "node_results": [
            {
                "node_id": "NODE-0001",
                "worker_id": "WORKER-0001",
                "plugin": "echo",
                "action": "package",
                "status": "complete",
                "outputs": ["", None, "echo://NODE-0001"],
            }
        ]
    }
    collector = ArtifactCollector(ArtifactStore())

    artifacts = collector.collect_from_execution(execution)

    assert [artifact.uri for artifact in artifacts] == ["echo://NODE-0001"]
