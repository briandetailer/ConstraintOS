from runtime import RuntimeState, runtime_result_to_trace
from runtime.result import RuntimeResult
from runtime.events import RuntimeEvent, RuntimeEventType


def test_runtime_traceability_maps_completed_runtime_result() -> None:
    result = RuntimeResult(
        id="RUNTIME-0001",
        status=RuntimeState.COMPLETED,
        success=True,
        plan={
            "execution_plan": {"id": "PLAN-0001"},
            "nodes": [{"id": "NODE-0001"}],
            "stages": [{"id": "STAGE-0001"}],
        },
        schedule={
            "schedule_result": {"id": "SCHEDULE-0001"},
            "assignments": [{"node_id": "NODE-0001", "worker_id": "WORKER-0001"}],
            "unscheduled_nodes": [],
        },
        execution={
            "execution_result": {"id": "EXEC-RESULT-0001"},
            "node_results": [
                {"node_id": "NODE-0001", "worker_id": "WORKER-0001", "plugin": "echo", "status": "complete"}
            ],
        },
        artifacts={
            "artifact_store": {"count": 1},
            "artifacts": [{"id": "ARTIFACT-0001", "uri": "echo://NODE-0001", "kind": "file", "producer": "NODE-0001"}],
        },
        events=[RuntimeEvent(RuntimeEventType.RUNTIME_STARTED, {"runtime_id": "RUNTIME-0001"})],
    )

    trace = runtime_result_to_trace(result)
    data = trace.to_dict()

    assert data["runtime_traceability"] == {
        "runtime_id": "RUNTIME-0001",
        "status": "completed",
        "success": True,
        "record_count": 5,
    }
    assert [record["type"] for record in data["records"]] == [
        "plan_node",
        "scheduled_assignment",
        "node_result",
        "artifact",
        "runtime_event",
    ]
    assert data["records"][0]["parent_id"] == "PLAN-0001"
    assert data["records"][1]["parent_id"] == "SCHEDULE-0001"
    assert data["records"][2]["parent_id"] == "EXEC-RESULT-0001"
    assert data["records"][3]["parent_id"] == "NODE-0001"


def test_runtime_traceability_maps_partial_unscheduled_nodes() -> None:
    trace = runtime_result_to_trace(
        {
            "runtime_result": {"id": "RUNTIME-0002", "status": "partial", "success": False},
            "schedule": {
                "schedule_result": {"id": "SCHEDULE-0002"},
                "assignments": [],
                "unscheduled_nodes": ["NODE-0002"],
            },
            "events": [{"event_type": "runtime_failed"}],
        }
    )
    data = trace.to_dict()

    assert data["runtime_traceability"]["status"] == "partial"
    assert data["runtime_traceability"]["success"] is False
    assert [record["type"] for record in data["records"]] == ["unscheduled_node", "runtime_event"]
    assert data["records"][0]["source_id"] == "NODE-0002"
    assert data["records"][0]["status"] == "unscheduled"


def test_runtime_traceability_maps_failed_runtime_without_optional_payloads() -> None:
    trace = runtime_result_to_trace({"runtime_result": {"id": "RUNTIME-0003", "status": "failed", "success": False}})

    assert trace.to_dict() == {
        "runtime_traceability": {
            "runtime_id": "RUNTIME-0003",
            "status": "failed",
            "success": False,
            "record_count": 0,
        },
        "records": [],
    }
