import json

from runtime import RuntimeEngine, RuntimeState, runtime_result_to_trace, verify_runtime_trace
from runtime.artifacts import ArtifactStore, RuntimeReportWriter
from runtime.scheduler import WorkerCapability


def test_completed_runtime_report_round_trips_to_valid_trace(tmp_path) -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [
            {"id": "NODE-0001", "plugin": "generic", "action": "prepare"},
            {"id": "NODE-0002", "plugin": "generic", "action": "package", "depends_on": ["NODE-0001"]},
        ],
    }
    result = RuntimeEngine().run(specification, [WorkerCapability("WORKER-0001", ["generic"])])
    report = RuntimeReportWriter(ArtifactStore(tmp_path)).write_report(result)
    report_data = json.loads((tmp_path / "reports" / "RUNTIME-0001.json").read_text(encoding="utf-8"))

    trace = runtime_result_to_trace(report_data)
    verification = verify_runtime_trace(trace)
    trace_data = trace.to_dict()

    assert result.status == RuntimeState.COMPLETED
    assert report.metadata["runtime_status"] == "completed"
    assert verification.successful() is True
    assert trace_data["runtime_traceability"]["runtime_id"] == report.metadata["runtime_id"]
    assert trace_data["runtime_traceability"]["record_count"] == len(trace_data["records"])
    assert {record["type"] for record in trace_data["records"]} >= {
        "plan_node",
        "scheduled_assignment",
        "node_result",
        "artifact",
        "runtime_event",
    }


def test_partial_runtime_report_round_trips_to_valid_trace(tmp_path) -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [{"id": "NODE-0001", "plugin": "blender", "action": "render"}],
    }
    result = RuntimeEngine().run(specification, [WorkerCapability("WORKER-0001", ["generic"])])
    report = RuntimeReportWriter(ArtifactStore(tmp_path)).write_report(result)
    report_data = json.loads((tmp_path / "reports" / "RUNTIME-0001.json").read_text(encoding="utf-8"))

    trace = runtime_result_to_trace(report_data)
    verification = verify_runtime_trace(trace)
    trace_data = trace.to_dict()

    assert result.status == RuntimeState.PARTIAL
    assert report.metadata["runtime_status"] == "partial"
    assert verification.successful() is True
    assert trace_data["runtime_traceability"]["success"] is False
    assert [record["type"] for record in trace_data["records"]].count("unscheduled_node") == 1
    assert [record["status"] for record in trace_data["records"] if record["type"] == "unscheduled_node"] == [
        "unscheduled"
    ]
