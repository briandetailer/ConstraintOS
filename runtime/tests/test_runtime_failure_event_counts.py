from runtime import RuntimeEngine
from runtime.scheduler import WorkerCapability


def test_runtime_failed_event_includes_unscheduled_count() -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [
            {"id": "NODE-0001", "plugin": "missing", "action": "render"},
            {"id": "NODE-0002", "plugin": "missing", "action": "package"},
        ],
    }

    result = RuntimeEngine().run(specification, [WorkerCapability("WORKER-0001", ["generic"])])

    failed_events = [event for event in result.to_dict()["events"] if event["event_type"] == "runtime_failed"]

    assert len(failed_events) == 1
    assert failed_events[0]["payload"]["unscheduled_nodes"] == ["NODE-0001", "NODE-0002"]
    assert failed_events[0]["payload"]["unscheduled_count"] == 2
    assert result.execution is None
