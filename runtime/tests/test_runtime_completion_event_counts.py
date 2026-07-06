from runtime import RuntimeEngine
from runtime.scheduler import WorkerCapability


def test_runtime_completed_event_includes_result_and_artifact_counts() -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [
            {"id": "NODE-0001", "plugin": "generic", "action": "prepare"},
            {"id": "NODE-0002", "plugin": "generic", "action": "package", "depends_on": ["NODE-0001"]},
        ],
    }

    result = RuntimeEngine().run(specification, [WorkerCapability("WORKER-0001", ["generic"])])

    completed_events = [event for event in result.to_dict()["events"] if event["event_type"] == "runtime_completed"]

    assert len(completed_events) == 1
    assert completed_events[0]["payload"]["node_results"] == 2
    assert completed_events[0]["payload"]["artifacts"] == 2
    assert completed_events[0]["payload"]["execution_result_id"] == "RUNTIME-0001-EXEC-RESULT-0001"
