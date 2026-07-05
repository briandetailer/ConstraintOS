import pytest

from runtime.artifacts import ArtifactStore, ArtifactStoreError, RuntimeArtifact


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
