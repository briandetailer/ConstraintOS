from runtime import RuntimeContext, RuntimeEngine, RuntimeState, runtime_result_to_trace, verify_runtime_trace
from runtime.scheduler import WorkerCapability


def test_runtime_engine_completed_result_maps_to_valid_trace() -> None:
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
    trace = runtime_result_to_trace(result)
    data = trace.to_dict()

    assert result.status == RuntimeState.COMPLETED
    assert verify_runtime_trace(trace).successful() is True
    assert data["runtime_traceability"]["status"] == "completed"
    assert data["runtime_traceability"]["success"] is True
    assert data["runtime_traceability"]["record_count"] == 13
    assert [record["type"] for record in data["records"]].count("plan_node") == 2
    assert [record["type"] for record in data["records"]].count("scheduled_assignment") == 2
    assert [record["type"] for record in data["records"]].count("node_result") == 2
    assert [record["type"] for record in data["records"]].count("artifact") == 2
    assert [record["type"] for record in data["records"]].count("runtime_event") == 5


def test_runtime_engine_partial_result_maps_to_valid_trace() -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [{"id": "NODE-0001", "plugin": "blender", "action": "render"}],
    }

    result = RuntimeEngine().run(specification, [WorkerCapability("WORKER-0001", ["generic"])])
    trace = runtime_result_to_trace(result)
    data = trace.to_dict()

    assert result.status == RuntimeState.PARTIAL
    assert verify_runtime_trace(trace).successful() is True
    assert data["runtime_traceability"]["status"] == "partial"
    assert data["runtime_traceability"]["success"] is False
    assert [record["type"] for record in data["records"]] == [
        "plan_node",
        "unscheduled_node",
        "runtime_event",
        "runtime_event",
        "runtime_event",
        "runtime_event",
    ]


def test_runtime_engine_failed_result_maps_to_valid_trace() -> None:
    result = RuntimeEngine().run(
        {"execution_steps": [{"id": "NODE-0001", "plugin": "generic"}]},
        [WorkerCapability("WORKER-0001", ["generic"])],
    )
    trace = runtime_result_to_trace(result)
    data = trace.to_dict()

    assert result.status == RuntimeState.FAILED
    assert verify_runtime_trace(trace).successful() is True
    assert data["runtime_traceability"]["status"] == "failed"
    assert data["runtime_traceability"]["success"] is False
    assert [record["type"] for record in data["records"]] == ["runtime_event", "runtime_event"]
