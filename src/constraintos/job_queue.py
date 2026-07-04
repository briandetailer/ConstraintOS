from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class QueueRecord:
    id: str
    job_type: str
    payload: dict[str, Any]
    status: str = "queued"
    priority: int = 5

    def to_dict(self) -> dict[str, Any]:
        return {
            "queue_record": {
                "id": self.id,
                "job_type": self.job_type,
                "status": self.status,
                "priority": self.priority,
                "created": date.today().isoformat(),
            },
            "payload": self.payload,
        }


class InMemoryJobQueue:
    def __init__(self) -> None:
        self._jobs: dict[str, QueueRecord] = {}

    def enqueue(self, job_id: str, job_type: str, payload: dict[str, Any], priority: int = 5) -> QueueRecord:
        if job_id in self._jobs:
            raise ValueError(f"Job already exists: {job_id}")
        record = QueueRecord(id=job_id, job_type=job_type, payload=payload, priority=priority)
        self._jobs[job_id] = record
        return record

    def get(self, job_id: str) -> QueueRecord | None:
        return self._jobs.get(job_id)

    def update_status(self, job_id: str, status: str) -> QueueRecord:
        if job_id not in self._jobs:
            raise KeyError(f"Job not found: {job_id}")
        record = self._jobs[job_id]
        updated = QueueRecord(
            id=record.id,
            job_type=record.job_type,
            payload=record.payload,
            status=status,
            priority=record.priority,
        )
        self._jobs[job_id] = updated
        return updated

    def list_jobs(self) -> list[QueueRecord]:
        return sorted(self._jobs.values(), key=lambda job: (job.priority, job.id))


def create_queue_status(queue_name: str, queued: int, running: int = 0, complete: int = 0, failed: int = 0) -> dict[str, Any]:
    return {
        "queue_status": {
            "name": queue_name,
            "created": date.today().isoformat(),
            "queued": queued,
            "running": running,
            "complete": complete,
            "failed": failed,
        }
    }
