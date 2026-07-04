from constraintos.observability import create_runtime_health_report, summarize_failures, summarize_queue, summarize_worker_fleet


def test_summarize_worker_fleet() -> None:
    report = summarize_worker_fleet([
        {"worker_heartbeat": {"status": "available"}},
        {"worker_heartbeat": {"status": "busy"}},
    ])
    assert report["worker_fleet_status"]["total"] == 2
    assert report["worker_fleet_status"]["available"] == 1


def test_summarize_queue() -> None:
    report = summarize_queue([
        {"queue_record": {"status": "queued"}},
        {"queue_record": {"status": "failed"}},
    ])
    assert report["job_queue_summary"]["total"] == 2
    assert report["job_queue_summary"]["queued"] == 1


def test_summarize_failures() -> None:
    report = summarize_failures([
        {"failed_job": {"failure_class": "missing_input"}},
        {"failed_job": {"failure_class": "runtime_failure"}},
    ])
    assert report["failure_summary_report"]["total"] == 2
    assert report["failure_summary_report"]["missing_input"] == 1


def test_create_runtime_health_report_degraded_without_workers() -> None:
    report = create_runtime_health_report("HEALTH-0001", [], [], [])
    assert report["runtime_health_report"]["status"] == "degraded"


def test_create_runtime_health_report_ok() -> None:
    report = create_runtime_health_report(
        "HEALTH-0001",
        [{"queue_record": {"status": "queued"}}],
        [{"worker_heartbeat": {"status": "available"}}],
        [],
    )
    assert report["runtime_health_report"]["status"] == "ok"
