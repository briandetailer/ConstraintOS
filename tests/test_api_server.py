from constraintos.api_server import (
    compile_payload,
    enqueue_job_payload,
    get_job_payload,
    health_payload,
    queue_status_payload,
    validate_payload,
    volume_build_payload,
)


def sample_spec() -> dict:
    return {
        "artifact": {"id": "PLATE-0001", "title": "Test", "type": "technical_plate", "version": "0.1"},
        "constraints": [
            {"id": "C-0001", "statement": "Must show V6", "severity": "blocker", "acceptance": "V6 visible", "validation_method": "review"}
        ],
    }


def test_health_payload() -> None:
    payload = health_payload()
    assert payload["status"] == "ok"
    assert payload["service"] == "constraintos-api"


def test_compile_payload() -> None:
    result = compile_payload(sample_spec())
    assert result["artifact_id"] == "PLATE-0001"
    assert "Must show V6" in result["instruction"]


def test_validate_payload_stub() -> None:
    result = validate_payload({"artifact_ref": "example"})
    assert result["status"] == "stub"
    assert "Validation endpoint scaffold" in result["message"]


def test_volume_build_payload() -> None:
    plan = {
        "volume_plan": {"id": "VOLUME-0001", "max_iterations_per_plate": 3},
        "plates": [{"id": "PLATE-0001", "title": "Test", "specification_path": "test.yaml", "sequence": 1}],
        "build_policy": {"stop_on_blocked_plate": True},
    }
    result = volume_build_payload(plan, {"PLATE-0001": sample_spec()})
    assert result["volume_build"]["status"] == "complete"


def test_enqueue_and_get_job_payload() -> None:
    result = enqueue_job_payload("JOB-9991", "test", {"hello": "world"})
    assert result["queue_record"]["id"] == "JOB-9991"
    fetched = get_job_payload("JOB-9991")
    assert fetched["payload"]["hello"] == "world"


def test_queue_status_payload() -> None:
    status = queue_status_payload()
    assert "queue_status" in status
