from runtime import RuntimeEngine
from runtime.scheduler import WorkerCapability


def test_runtime_engine_derives_execution_ids_from_runtime_id() -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [{"id": "NODE-0001", "plugin": "generic", "action": "prepare"}],
    }

    result = RuntimeEngine().run(
        specification,
        [WorkerCapability("WORKER-0001", ["generic"])],
        runtime_id="RUNTIME-0042",
    )

    assert result.execution is not None
    assert result.execution["execution_result"]["id"] == "RUNTIME-0042-EXEC-RESULT-0001"
    assert result.execution["execution_result"]["request_id"] == "RUNTIME-0042-EXEC-REQ-0001"
