from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class RuntimeHealthReport:
    id: str
    status: str
    queue_status: dict[str, Any]
    worker_status: dict[str, Any]
    failure_status: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "runtime_health_report": {
                "id": self.id,
                "status": self.status,
                "created": date.today().isoformat(),
            },
            "queue_status": self.queue_status,
            "worker_status": self.worker_status,
            "failure_status": self.failure_status,
        }


def summarize_worker_fleet(heartbeats: list[dict[str, Any]]) -> dict[str, Any]:
    statuses = {"available": 0, "busy": 0, "offline": 0, "disabled": 0, "unknown": 0}
    for heartbeat in heartbeats:
        data = heartbeat.get("worker_heartbeat", heartbeat)
        status = data.get("status", "unknown")
        statuses[status if status in statuses else "unknown"] += 1
    return {"worker_fleet_status": {"created": date.today().isoformat(), "total": len(heartbeats), **statuses}}


def summarize_queue(records: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {"queued": 0, "running": 0, "complete": 0, "failed": 0, "blocked": 0, "unknown": 0}
    for record in records:
        data = record.get("queue_record", record)
        status = data.get("status", "unknown")
        counts[status if status in counts else "unknown"] += 1
    return {"queue_summary_report": {"created": date.today().isoformat(), "total": len(records), **counts}}


def summarize_failures(failed_jobs: list[dict[str, Any]]) -> dict[str, Any]:
    classes = {"unsupported_job_type": 0, "missing_input": 0, "validation_failure": 0, "runtime_failure": 0, "unknown": 0}
    for failed in failed_jobs:
        data = failed.get("failed_job", failed)
        failure_class = data.get("failure_class", "unknown")
        classes[failure_class if failure_class in classes else "unknown"] += 1
    return {"failure_summary_report": {"created": date.today().isoformat(), "total": len(failed_jobs), **classes}}


def create_runtime_health_report(report_id: str, queue_records: list[dict[str, Any]], heartbeats: list[dict[str, Any]], failed_jobs: list[dict[str, Any]]) -> dict[str, Any]:
    queue_status = summarize_queue(queue_records)
    worker_status = summarize_worker_fleet(heartbeats)
    failure_status = summarize_failures(failed_jobs)
    status = "ok"
    if failure_status["failure_summary_report"].get("total", 0) > 0:
        status = "degraded"
    if worker_status["worker_fleet_status"].get("total", 0) == 0:
        status = "degraded"
    return RuntimeHealthReport(report_id, status, queue_status, worker_status, failure_status).to_dict()
