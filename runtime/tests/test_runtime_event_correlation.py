from runtime import RuntimeEngine
from runtime.scheduler import WorkerCapability


def test_runtime_execution_started_event_includes_request_id() -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [{"id": "NODE-0001", "plugin": "generic", "action": "prepare"}],
    }

    result = RuntimeEngine().run(
        specification,
        [WorkerCapability("WORKER-0001", ["generic"])],
        runtime_id="RUNTIME-0043",
    )

    event_data = result.to_dict()["events"]
    execution_started = [event for event in event_data if event["event_type"] == "runtime_execution_started"]

    assert execution_started == [
        {
            "timestamp": execution_started[0]["timestamp"],
            "event_type": "runtime_execution_started",
            "payload": {
                "schedule_id": "SCHEDULE-0001",
                "execution_request_id": "RUNTIME-0043-EXEC-REQ-0001",
            },
        }
    ]
