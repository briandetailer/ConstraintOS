from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Callable

from constraintos.atlas_builder import run_volume_dry_build
from constraintos.job_queue import QueueRecord


@dataclass
class WorkerResult:
    id: str
    job_id: str
    worker_id: str
    status: str
    output: dict[str, Any]
    messages: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "worker_result": {
                "id": self.id,
                "job_id": self.job_id,
                "worker_id": self.worker_id,
                "status": self.status,
                "created": date.today().isoformat(),
            },
            "output": self.output,
            "messages": self.messages,
        }


class WorkerRegistry:
    def __init__(self) -> None:
        self._handlers: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {}

    def register(self, job_type: str, handler: Callable[[dict[str, Any]], dict[str, Any]]) -> None:
        self._handlers[job_type] = handler

    def supports(self, job_type: str) -> bool:
        return job_type in self._handlers

    def dispatch(self, job_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        if job_type not in self._handlers:
            raise ValueError(f"Unsupported job type: {job_type}")
        return self._handlers[job_type](payload)


def volume_build_handler(payload: dict[str, Any]) -> dict[str, Any]:
    volume_plan = payload.get("volume_plan_payload", payload.get("volume_plan", payload))
    specs = payload.get("specs_by_artifact_id", {})
    return run_volume_dry_build(volume_plan, specs)


def create_default_worker_registry() -> WorkerRegistry:
    registry = WorkerRegistry()
    registry.register("volume_build", volume_build_handler)
    return registry


def execute_job(record: QueueRecord, worker_id: str = "WORKER-0001", registry: WorkerRegistry | None = None) -> WorkerResult:
    active_registry = registry or create_default_worker_registry()
    try:
        output = active_registry.dispatch(record.job_type, record.payload)
        status = "complete"
        messages = ["Job executed successfully."]
    except Exception as exc:  # pragma: no cover - behavior tested via unsupported job
        output = {}
        status = "failed"
        messages = [str(exc)]
    return WorkerResult(
        id=f"RESULT-{record.id}",
        job_id=record.id,
        worker_id=worker_id,
        status=status,
        output=output,
        messages=messages,
    )
