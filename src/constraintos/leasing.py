from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any


UTC = timezone.utc


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


@dataclass
class WorkerHeartbeat:
    worker_id: str
    status: str
    active_job_id: str | None = None
    timestamp: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "worker_heartbeat": {
                "worker_id": self.worker_id,
                "status": self.status,
                "active_job_id": self.active_job_id,
                "timestamp": self.timestamp or now_iso(),
            }
        }


@dataclass
class JobLease:
    id: str
    job_id: str
    worker_id: str
    status: str
    acquired_at: str
    expires_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "job_lease": {
                "id": self.id,
                "job_id": self.job_id,
                "worker_id": self.worker_id,
                "status": self.status,
                "acquired_at": self.acquired_at,
                "expires_at": self.expires_at,
            }
        }


def create_heartbeat(worker_id: str, status: str = "available", active_job_id: str | None = None) -> WorkerHeartbeat:
    return WorkerHeartbeat(worker_id=worker_id, status=status, active_job_id=active_job_id, timestamp=now_iso())


def acquire_lease(job_id: str, worker_id: str, lease_id: str = "LEASE-0001", ttl_seconds: int = 300) -> JobLease:
    acquired = datetime.now(UTC).replace(microsecond=0)
    expires = acquired + timedelta(seconds=ttl_seconds)
    return JobLease(
        id=lease_id,
        job_id=job_id,
        worker_id=worker_id,
        status="active",
        acquired_at=acquired.isoformat(),
        expires_at=expires.isoformat(),
    )


def is_lease_expired(lease: JobLease | dict[str, Any], at_time: datetime | None = None) -> bool:
    data = lease.to_dict()["job_lease"] if isinstance(lease, JobLease) else lease.get("job_lease", lease)
    expires_at = datetime.fromisoformat(str(data["expires_at"]))
    current = at_time or datetime.now(UTC)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=UTC)
    if current.tzinfo is None:
        current = current.replace(tzinfo=UTC)
    return current >= expires_at


def heartbeat_is_stale(heartbeat: WorkerHeartbeat | dict[str, Any], max_age_seconds: int = 120, at_time: datetime | None = None) -> bool:
    data = heartbeat.to_dict()["worker_heartbeat"] if isinstance(heartbeat, WorkerHeartbeat) else heartbeat.get("worker_heartbeat", heartbeat)
    timestamp = datetime.fromisoformat(str(data["timestamp"]))
    current = at_time or datetime.now(UTC)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=UTC)
    if current.tzinfo is None:
        current = current.replace(tzinfo=UTC)
    return current - timestamp > timedelta(seconds=max_age_seconds)


def create_lease_decision(lease: JobLease | dict[str, Any], heartbeat: WorkerHeartbeat | dict[str, Any] | None = None) -> dict[str, Any]:
    lease_data = lease.to_dict()["job_lease"] if isinstance(lease, JobLease) else lease.get("job_lease", lease)
    expired = is_lease_expired(lease)
    stale = heartbeat_is_stale(heartbeat) if heartbeat is not None else False
    if expired or stale:
        decision = "release"
        reason = "lease expired" if expired else "worker heartbeat stale"
    else:
        decision = "keep"
        reason = "lease active and worker healthy"
    return {
        "lease_decision": {
            "lease_id": lease_data.get("id"),
            "job_id": lease_data.get("job_id"),
            "worker_id": lease_data.get("worker_id"),
            "decision": decision,
            "reason": reason,
            "created": now_iso(),
        }
    }
