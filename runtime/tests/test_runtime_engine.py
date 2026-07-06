from runtime import (
    RuntimeContext,
    RuntimeEngine,
    RuntimeState,
    verify_partial_schedule_runtime_events,
    verify_successful_runtime_events,
)
from runtime.scheduler import WorkerCapability


SUCCESSFUL_RUNTIME_EVENT_ORDER = [
    "runtime_started",
    "runtime_planned",
    "runtime_scheduled",
    "runtime_execution_started",
    "runtime_completed",
]

PARTIAL_SCHEDULE_RUNTIME_EVENT_ORDER = [
    "runtime_started",
    "runtime_planned",
    "runtime_scheduled",
    "runtime_failed",
]


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
    replay_verification = verify_successful_runtime_events(result)

    assert result.status == RuntimeState.COMPLETED
    assert result.success is True
    assert data["runtime_result"]["status"] == "completed"
    assert data["plan"]["execution_plan"]["status"] == "planned"
    assert data["schedule"]["schedule_result"]["status"] == "scheduled"
    assert data["execution"]["execution_result"]["status"] == "complete"
    assert replay_verification.successful() is True
    assert replay_verification.event_types == SUCCESSFUL_RUNTIME_EVENT_ORDER


def test_runtime_replay_verifier_reports_success_event_order_mismatch() -> None:
    replay_verification = verify_successful_runtime_events(
        {
            "events": [
                {"event_type": "runtime_started"},
                {"event_type": "runtime_planned"},
                {"event_type": "runtime_completed"},
            ]
        }
    )

    assert replay_verification.successful() is False
    assert replay_verification.expected_event_types == SUCCESSFUL_RUNTIME_EVENT_ORDER
    assert replay_verification.issues == [
        "Successful runtime event order mismatch: "
        "expected ['runtime_started', 'runtime_planned', 'runtime_scheduled', "
        "'runtime_execution_started', 'runtime_completed'], "
        "received ['runtime_started', 'runtime_planned', 'runtime_completed']."
    ]


def test_runtime_engine_stops_before_execution_when_schedule_is_partial() -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [{"id": "NODE-0001", "plugin": "blender", "action": "render"}],
    }
    result = RuntimeEngine().run(specification, [WorkerCapability("WORKER-0001", ["generic"])])
    replay_verification = verify_partial_schedule_runtime_events(result)

    assert result.status == RuntimeState.PARTIAL
    assert result.success is False
    assert result.execution is None
    assert result.schedule is not None
    assert result.schedule["unscheduled_nodes"] == ["NODE-0001"]
    assert result.messages == ["Runtime schedule contains unscheduled nodes; execution was not started."]
    assert replay_verification.successful() is True
    assert replay_verification.event_types == PARTIAL_SCHEDULE_RUNTIME_EVENT_ORDER


def test_runtime_replay_verifier_reports_partial_schedule_payload_mismatch() -> None:
    replay_verification = verify_partial_schedule_runtime_events(
        {
            "runtime_result": {"status": "partial"},
            "schedule": {"unscheduled_nodes": ["NODE-0001"]},
            "execution": None,
            "events": [
                {"event_type": "runtime_started"},
                {"event_type": "runtime_planned"},
                {"event_type": "runtime_scheduled"},
                {
                    "event_type": "runtime_failed",
                    "payload": {"unscheduled_nodes": ["NODE-0001", "NODE-0002"], "unscheduled_count": 1},
                },
            ],
        }
    )

    assert replay_verification.successful() is False
    assert replay_verification.expected_event_types == PARTIAL_SCHEDULE_RUNTIME_EVENT_ORDER
    assert replay_verification.issues == [
        "Partial schedule runtime_failed unscheduled_count must match unscheduled_nodes length.",
        "Partial schedule runtime_failed unscheduled_nodes must match schedule unscheduled_nodes.",
    ]


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
