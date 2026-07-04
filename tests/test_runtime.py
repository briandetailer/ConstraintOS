from constraintos.runtime import RuntimeJob, WorkerProfile, create_metric_event, create_runtime_config


def test_runtime_job_model() -> None:
    job = RuntimeJob("JOB-0001", "volume_build", "examples/volumes/VOLUME-0001.yaml")
    data = job.to_dict()
    assert data["runtime_job"]["id"] == "JOB-0001"
    assert data["runtime_job"]["status"] == "queued"


def test_worker_profile_model() -> None:
    worker = WorkerProfile("WORKER-0001", "dry-run", ["compile", "render", "validate"])
    data = worker.to_dict()
    assert data["worker_profile"]["id"] == "WORKER-0001"
    assert "render" in data["worker_profile"]["capabilities"]


def test_runtime_config_boundaries() -> None:
    config = create_runtime_config(api_enabled=True)
    assert config["runtime_config"]["api_enabled"] is True
    assert config["boundaries"]["kernel_owns_auth"] is False
    assert config["boundaries"]["runtime_calls_kernel"] is True


def test_metric_event_model() -> None:
    metric = create_metric_event("METRIC-0001", "build.duration.seconds", 12.5, {"volume": "VOLUME-0001"})
    assert metric["metric_event"]["name"] == "build.duration.seconds"
    assert metric["dimensions"]["volume"] == "VOLUME-0001"
