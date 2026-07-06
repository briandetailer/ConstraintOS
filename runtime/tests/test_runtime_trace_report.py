import json

import pytest

from runtime import RuntimeEngine, RuntimeState, RuntimeTraceReportWriter, runtime_result_to_trace
from runtime.artifacts import ArtifactStore
from runtime.scheduler import WorkerCapability


def test_runtime_trace_report_writer_persists_generated_trace(tmp_path) -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [{"id": "NODE-0001", "plugin": "generic", "action": "prepare"}],
    }
    result = RuntimeEngine().run(specification, [WorkerCapability("WORKER-0001", ["generic"])])
    trace = runtime_result_to_trace(result)
    writer = RuntimeTraceReportWriter(ArtifactStore(tmp_path))

    artifact = writer.write_trace(trace)
    trace_path = tmp_path / "traces" / "RUNTIME-0001.json"
    trace_data = json.loads(trace_path.read_text(encoding="utf-8"))

    assert result.status == RuntimeState.COMPLETED
    assert artifact.producer == "RUNTIME-0001"
    assert artifact.metadata["artifact_role"] == "runtime_trace_report"
    assert artifact.metadata["content_type"] == "application/json"
    assert artifact.metadata["runtime_id"] == "RUNTIME-0001"
    assert artifact.metadata["trace_status"] == "completed"
    assert artifact.metadata["trace_success"] is True
    assert artifact.metadata["record_count"] == trace.to_dict()["runtime_traceability"]["record_count"]
    assert artifact.metadata["path"] == str(trace_path.resolve())
    assert trace_data == trace.to_dict()


def test_runtime_trace_report_writer_maps_runtime_result_and_uses_custom_path(tmp_path) -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [{"id": "NODE-0001", "plugin": "blender", "action": "render"}],
    }
    result = RuntimeEngine().run(specification, [WorkerCapability("WORKER-0001", ["generic"])])
    writer = RuntimeTraceReportWriter(ArtifactStore(tmp_path))

    artifact = writer.write_trace(result, relative_path="custom/runtime-trace.json")
    trace_path = tmp_path / "custom" / "runtime-trace.json"
    trace_data = json.loads(trace_path.read_text(encoding="utf-8"))

    assert result.status == RuntimeState.PARTIAL
    assert artifact.uri == trace_path.resolve().as_uri()
    assert artifact.metadata["trace_status"] == "partial"
    assert artifact.metadata["trace_success"] is False
    assert [record["type"] for record in trace_data["records"]].count("unscheduled_node") == 1


def test_runtime_trace_report_writer_rejects_invalid_trace(tmp_path) -> None:
    writer = RuntimeTraceReportWriter(ArtifactStore(tmp_path))

    with pytest.raises(ValueError, match="Runtime trace report requires a valid runtime trace"):
        writer.write_trace({"runtime_traceability": {"runtime_id": "RUNTIME-0001", "record_count": 1}, "records": []})
