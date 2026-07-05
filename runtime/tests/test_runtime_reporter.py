import json

from runtime import RuntimeReportWriter, RuntimeResult, RuntimeState
from runtime.artifacts import ArtifactStore


def test_runtime_report_writer_writes_runtime_result_json(tmp_path) -> None:
    store = ArtifactStore(tmp_path)
    writer = RuntimeReportWriter(store)
    result = RuntimeResult(
        id="RUNTIME-0001",
        status=RuntimeState.COMPLETED,
        success=True,
        messages=["Runtime completed successfully."],
    )

    artifact = writer.write_report(result)

    written = tmp_path / "reports" / "RUNTIME-0001.json"
    data = json.loads(written.read_text(encoding="utf-8"))
    assert artifact.uri == written.resolve().as_uri()
    assert artifact.producer == "RUNTIME-0001"
    assert artifact.metadata["content_type"] == "application/json"
    assert artifact.metadata["artifact_role"] == "runtime_report"
    assert data["runtime_result"]["id"] == "RUNTIME-0001"
    assert data["runtime_result"]["status"] == "completed"


def test_runtime_report_writer_accepts_plain_dictionary(tmp_path) -> None:
    writer = RuntimeReportWriter(ArtifactStore(tmp_path))

    artifact = writer.write_report({"runtime_result": {"id": "RUNTIME-0002"}}, "custom/report.json")

    written = tmp_path / "custom" / "report.json"
    data = json.loads(written.read_text(encoding="utf-8"))
    assert artifact.producer == "RUNTIME-0002"
    assert artifact.metadata["runtime_id"] == "RUNTIME-0002"
    assert data["runtime_result"]["id"] == "RUNTIME-0002"


def test_runtime_report_writer_uses_unknown_runtime_id_when_missing(tmp_path) -> None:
    writer = RuntimeReportWriter(ArtifactStore(tmp_path))

    artifact = writer.write_report({"messages": []})

    assert artifact.producer == "RUNTIME-UNKNOWN"
    assert artifact.metadata["runtime_id"] == "RUNTIME-UNKNOWN"
