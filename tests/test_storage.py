from pathlib import Path

from constraintos.storage import LocalStorageBackend, create_artifact_repository_layout


def test_local_storage_put_and_get_text(tmp_path: Path) -> None:
    backend = LocalStorageBackend(tmp_path)
    stored = backend.put_text("OUTPUT-1.txt", "hello", "text/plain")
    assert stored.id == "OUTPUT-1.txt"
    assert stored.size_bytes == 5
    assert backend.get_text("OUTPUT-1.txt") == "hello"


def test_local_storage_sanitizes_path(tmp_path: Path) -> None:
    backend = LocalStorageBackend(tmp_path)
    backend.put_text("../bad.txt", "safe")
    assert (tmp_path / "__bad.txt").exists()


def test_create_artifact_repository_layout(tmp_path: Path) -> None:
    layout = create_artifact_repository_layout(tmp_path)
    assert (tmp_path / "outputs").exists()
    assert "manifests" in layout
    assert "baselines" in layout
