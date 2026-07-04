from datetime import datetime, timedelta, timezone

from constraintos.leasing import acquire_lease, create_heartbeat, create_lease_decision, heartbeat_is_stale, is_lease_expired


def test_create_heartbeat() -> None:
    heartbeat = create_heartbeat("WORKER-0001", "available")
    data = heartbeat.to_dict()
    assert data["worker_heartbeat"]["worker_id"] == "WORKER-0001"
    assert data["worker_heartbeat"]["status"] == "available"


def test_acquire_lease() -> None:
    lease = acquire_lease("JOB-0001", "WORKER-0001", "LEASE-0001", ttl_seconds=60)
    data = lease.to_dict()
    assert data["job_lease"]["id"] == "LEASE-0001"
    assert data["job_lease"]["status"] == "active"


def test_lease_expiration() -> None:
    lease = acquire_lease("JOB-0001", "WORKER-0001", "LEASE-0001", ttl_seconds=1)
    future = datetime.now(timezone.utc) + timedelta(seconds=2)
    assert is_lease_expired(lease, at_time=future) is True


def test_heartbeat_stale() -> None:
    old = (datetime.now(timezone.utc) - timedelta(seconds=300)).replace(microsecond=0).isoformat()
    heartbeat = {"worker_heartbeat": {"worker_id": "WORKER-0001", "status": "busy", "active_job_id": "JOB-0001", "timestamp": old}}
    assert heartbeat_is_stale(heartbeat, max_age_seconds=120) is True


def test_lease_decision_keep() -> None:
    lease = acquire_lease("JOB-0001", "WORKER-0001", "LEASE-0001", ttl_seconds=300)
    heartbeat = create_heartbeat("WORKER-0001", "busy", "JOB-0001")
    decision = create_lease_decision(lease, heartbeat)
    assert decision["lease_decision"]["decision"] == "keep"
