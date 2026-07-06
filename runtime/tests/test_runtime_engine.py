from runtime import RuntimeContext, RuntimeEngine, RuntimeState
from runtime.scheduler import WorkerCapability


def test_runtime_engine_runs_plan_schedule_execute_pipeline() -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [
            {"id": "NODE-0001", "plugin": "generic", "action": "prepare"},
            {"id": "NODE-0002", "plugin": "generic", "action": "package", "depends_on": ["NODE-0001"]},
        ],
    }
    result = RuntimeEngine().run(
        specification,
        [WorkerCapability("WORKER-0001", ["generic"])],
        RuntimeContext(variables={"dry_run": True}),
    )

    data = result.to_dict()
    assert result.status == RuntimeState.COMPLETED
    assert result.success is True
    assert data["runtime_result"]["status"] == "completed"
    assert data["plan"]["execution_plan"]["status"] == "planned"
    assert data["schedule"]["schedule_result"]["status"] == "scheduled"
    assert data["execution"]["execution_result"]["status"] == "complete"
    assert [event["event_type"] for event in data["events"]] == [
        "runtime_started",
        "runtime_planned",
        "runtime_scheduled",
        "runtime_execution_started",
        "runtime_completed",
    ]


def test_runtime_engine_stops_before_execution_when_schedule_is_partial() -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [{"id": "NODE-0001", "plugin": "blender", "action": "render"}],
    }
    result = RuntimeEngine().run(specification, [WorkerCapability("WORKER-0001", ["generic"])])

    assert result.status == RuntimeState.PARTIAL
    assert result.success is False
    assert result.execution is None
    assert result.schedule is not None
    assert result.schedule["unscheduled_nodes"] == ["NODE-0001"]
    assert result.messages == ["Runtime schedule contains unscheduled nodes; execution was not started."]


def test_runtime_engine_returns_failed_result_for_invalid_specification() -> None:
    result = RuntimeEngine().run(
        {"execution_steps": [{"id": "NODE-0001", "plugin": "generic"}]},
        [WorkerCapability("WORKER-0001", ["generic"])],
    )

    data = result.to_dict()
    failed_events = [event for event in data["events"] if event["event_type"] == "runtime_failed"]

    assert result.status == RuntimeState.FAILED
    assert result.success is False
    assert result.plan is None
    assert result.messages == ["Missing action for step 1"]
    assert failed_events[0]["payload"]["error_type"] == "PlanningError"
    assert failed_events[0]["payload"]["error"] == "Missing action for step 1"
