import json

from runtime import RuntimeResult, RuntimeState
from runtime.artifacts import ArtifactStore, RuntimeReportWriter


def test_runtime_report_writer_records_runtime_metadata(tmp_path) -> None:
    result = RuntimeResult(
        id="RUNTIME-0007",
        status=RuntimeState.COMPLETED,
        success=True,
        plan={"nodes": [{"id": "NODE-0001"}], "stages": [{"id": "STAGE-0001"}]},
        schedule={"assignments": [{"node_id": "NODE-0001"}], "unscheduled_nodes": []},
        execution={"node_results": [{"node_id": "NODE-0001"}]},
        artifacts={"artifacts": [{"id": "ARTIFACT-0001"}]},
    )
    store = ArtifactStore(tmp_path)
    writer = RuntimeReportWriter(store)

    artifact = writer.write_report(result)

    assert artifact.metadata["runtime_id"] == "RUNTIME-0007"
    assert artifact.metadata["runtime_status"] == "completed"
    assert artifact.metadata["runtime_success"] is True
    assert artifact.metadata["summary"]["plan_nodes"] == 1
    assert artifact.metadata["summary"]["node_results"] == 1
    assert artifact.metadata["artifact_role"] == "runtime_report"


def test_runtime_report_writer_persists_summary_in_json(tmp_path) -> None:
    result = RuntimeResult(id="RUNTIME-0008", status=RuntimeState.PARTIAL, success=False)
    writer = RuntimeReportWriter(ArtifactStore(tmp_path))

    artifact = writer.write_report(result)
    payload = json.loads((tmp_path / "reports" / "RUNTIME-0008.json").read_text(encoding="utf-8"))

    assert payload["runtime_result"]["id"] == "RUNTIME-0008"
    assert payload["summary"] == result.summary()
    assert artifact.metadata["runtime_status"] == "partial"
