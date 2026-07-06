from runtime import RuntimeState, runtime_result_to_trace, verify_runtime_trace
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
        events=[RuntimeEvent(RuntimeEventType.STARTED, {"runtime_id": "RUNTIME-0001"})],
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


def test_runtime_trace_verifier_accepts_generated_trace() -> None:
    trace = runtime_result_to_trace(
        {
            "runtime_result": {"id": "RUNTIME-0004", "status": "partial", "success": False},
            "schedule": {"schedule_result": {"id": "SCHEDULE-0004"}, "unscheduled_nodes": ["NODE-0004"]},
            "events": [{"event_type": "runtime_failed"}],
        }
    )

    verification = verify_runtime_trace(trace)

    assert verification.successful() is True
    assert verification.to_dict() == {
        "runtime_trace_verification": {"successful": True, "issue_count": 0},
        "issues": [],
    }


def test_runtime_trace_verifier_reports_contract_mismatches() -> None:
    verification = verify_runtime_trace(
        {
            "runtime_traceability": {"runtime_id": "RUNTIME-0005", "record_count": 1},
            "records": [
                {"id": "TRACE-0001", "type": "runtime_event", "source_id": "runtime_started", "runtime_id": "RUNTIME-0005", "status": "runtime_started"},
                {"id": "TRACE-0001", "type": "runtime_event", "source_id": "runtime_failed", "runtime_id": "RUNTIME-OTHER", "status": "runtime_failed", "metadata": []},
            ],
        }
    )

    assert verification.successful() is False
    assert verification.issues == [
        "Runtime traceability record_count must match records length.",
        "Runtime trace record 2 runtime_id must match trace runtime_id.",
        "Runtime trace record 2 metadata must be a dictionary.",
        "Runtime trace record ids must be unique.",
    ]
