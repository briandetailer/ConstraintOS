from constraintos.job_queue import QueueRecord
from constraintos.worker import create_default_worker_registry, execute_job, volume_build_handler


def sample_spec() -> dict:
    return {
        "artifact": {"id": "PLATE-0001", "title": "Test", "type": "technical_plate", "version": "0.1"},
        "constraints": [
            {"id": "C-0001", "statement": "Must show V6", "severity": "blocker", "acceptance": "V6 visible", "validation_method": "review"}
        ],
    }


def sample_plan() -> dict:
    return {
        "volume_plan": {"id": "VOLUME-0001", "max_iterations_per_plate": 3},
        "plates": [{"id": "PLATE-0001", "title": "Test", "specification_path": "test.yaml", "sequence": 1}],
        "build_policy": {"stop_on_blocked_plate": True},
    }


def test_default_registry_supports_volume_build() -> None:
    registry = create_default_worker_registry()
    assert registry.supports("volume_build") is True
    assert registry.supports("unknown") is False


def test_volume_build_handler() -> None:
    result = volume_build_handler({"volume_plan_payload": sample_plan(), "specs_by_artifact_id": {"PLATE-0001": sample_spec()}})
    assert result["volume_build"]["status"] == "complete"


def test_execute_job_success() -> None:
    record = QueueRecord("JOB-0001", "volume_build", {"volume_plan_payload": sample_plan(), "specs_by_artifact_id": {"PLATE-0001": sample_spec()}})
    result = execute_job(record)
    data = result.to_dict()
    assert data["worker_result"]["status"] == "complete"
    assert data["worker_result"]["job_id"] == "JOB-0001"


def test_execute_job_unsupported_type_fails() -> None:
    record = QueueRecord("JOB-0002", "unknown", {})
    result = execute_job(record)
    assert result.status == "failed"
    assert "Unsupported job type" in result.messages[0]
