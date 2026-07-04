from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class RuntimeJob:
    id: str
    job_type: str
    payload_ref: str
    status: str = "queued"
    priority: int = 5

    def to_dict(self) -> dict[str, Any]:
        return {
            "runtime_job": {
                "id": self.id,
                "job_type": self.job_type,
                "payload_ref": self.payload_ref,
                "status": self.status,
                "priority": self.priority,
                "created": date.today().isoformat(),
            }
        }


@dataclass
class WorkerProfile:
    id: str
    worker_type: str
    capabilities: list[str]
    status: str = "available"

    def to_dict(self) -> dict[str, Any]:
        return {
            "worker_profile": {
                "id": self.id,
                "worker_type": self.worker_type,
                "capabilities": self.capabilities,
                "status": self.status,
                "registered": date.today().isoformat(),
            }
        }


def create_runtime_config(environment: str = "local", api_enabled: bool = False, queue_backend: str = "in_memory", storage_backend: str = "local") -> dict[str, Any]:
    return {
        "runtime_config": {
            "environment": environment,
            "api_enabled": api_enabled,
            "queue_backend": queue_backend,
            "storage_backend": storage_backend,
            "created": date.today().isoformat(),
        },
        "boundaries": {
            "kernel_owns_auth": False,
            "kernel_owns_billing": False,
            "kernel_owns_tenancy": False,
            "runtime_calls_kernel": True,
        },
    }


def create_metric_event(event_id: str, name: str, value: float, dimensions: dict[str, str] | None = None) -> dict[str, Any]:
    return {
        "metric_event": {
            "id": event_id,
            "name": name,
            "value": value,
            "created": date.today().isoformat(),
        },
        "dimensions": dimensions or {},
    }
