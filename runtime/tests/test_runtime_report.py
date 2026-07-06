import json

from runtime.artifacts import ArtifactStore, RuntimeReportWriter
from runtime.result import RuntimeResult
from runtime.state import RuntimeState


def test_runtime_report_writer_records_report_artifact_contract(tmp_path) -> None:
    result = RuntimeResult(
        id="RUNTIME-0001",
        status=RuntimeState.COMPLETED,
        success=True,
        plan={"nodes": [{"id": "NODE-0001"}], "stages": [{"id": "STAGE-0001"}]},
        schedule={"assignments": [{"node_id": "NODE-0001"}], "unscheduled_nodes": []},
        execution={"node_results": [{"node_id": "NODE-0001", "outputs": ["echo://NODE-0001"]}]},
        artifacts={"artifact_store": {"count": 1}, "artifacts": [{"id": "ARTIFACT-0001"}]},
        messages=["done"],
    )
    writer = RuntimeReportWriter(ArtifactStore(tmp_path))

    artifact = writer.write_report(result)
    report_path = tmp_path / "reports" / "RUNTIME-0001.json"
    report_data = json.loads(report_path.read_text(encoding="utf-8"))
    result_data = result.to_dict()

    assert artifact.producer == "RUNTIME-0001"
    assert artifact.metadata["artifact_role"] == "runtime_report"
    assert artifact.metadata["content_type"] == "application/json"
    assert artifact.metadata["runtime_id"] == "RUNTIME-0001"
    assert artifact.metadata["runtime_status"] == "completed"
    assert artifact.metadata["runtime_success"] is True
    assert artifact.metadata["summary"] == result_data["summary"]
    assert artifact.metadata["path"] == str(report_path.resolve())
    assert report_data == result_data


def test_runtime_report_writer_uses_custom_report_path(tmp_path) -> None:
    result = RuntimeResult(id="RUNTIME-0002", status=RuntimeState.FAILED, success=False)
    writer = RuntimeReportWriter(ArtifactStore(tmp_path))

    artifact = writer.write_report(result, relative_path="custom/runtime-report.json")
    report_path = tmp_path / "custom" / "runtime-report.json"

    assert artifact.uri == report_path.resolve().as_uri()
    assert artifact.metadata["runtime_id"] == "RUNTIME-0002"
    assert artifact.metadata["runtime_status"] == "failed"
    assert artifact.metadata["runtime_success"] is False
    assert json.loads(report_path.read_text(encoding="utf-8")) == result.to_dict()
