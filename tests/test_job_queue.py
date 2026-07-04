import pytest

from constraintos.job_queue import InMemoryJobQueue, create_queue_status


def test_enqueue_and_get_job() -> None:
    queue = InMemoryJobQueue()
    record = queue.enqueue("JOB-0001", "volume_build", {"volume": "VOLUME-0001"})
    assert record.id == "JOB-0001"
    assert queue.get("JOB-0001") is record


def test_duplicate_job_rejected() -> None:
    queue = InMemoryJobQueue()
    queue.enqueue("JOB-0001", "volume_build", {})
    with pytest.raises(ValueError):
        queue.enqueue("JOB-0001", "volume_build", {})


def test_update_status() -> None:
    queue = InMemoryJobQueue()
    queue.enqueue("JOB-0001", "volume_build", {})
    updated = queue.update_status("JOB-0001", "running")
    assert updated.status == "running"


def test_queue_status() -> None:
    status = create_queue_status("default", queued=2, running=1)
    assert status["queue_status"]["queued"] == 2
    assert status["queue_status"]["running"] == 1
