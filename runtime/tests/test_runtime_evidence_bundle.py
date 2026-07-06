import json

from runtime import RuntimeEngine, RuntimeEvidenceBundleWriter, RuntimeState, verify_runtime_evidence_manifest
from runtime.artifacts import ArtifactStore
from runtime.scheduler import WorkerCapability


def test_runtime_evidence_bundle_writer_links_runtime_and_trace_reports(tmp_path) -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [{"id": "NODE-0001", "plugin": "generic", "action": "prepare"}],
    }
    result = RuntimeEngine().run(specification, [WorkerCapability("WORKER-0001", ["generic"])])
    store = ArtifactStore(tmp_path)
    writer = RuntimeEvidenceBundleWriter(store)

    manifest_artifact = writer.write_evidence(result)
    manifest_path = tmp_path / "evidence" / "RUNTIME-0001.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result.status == RuntimeState.COMPLETED
    assert manifest_artifact.producer == "RUNTIME-0001"
    assert manifest_artifact.metadata["artifact_role"] == "runtime_evidence_manifest"
    assert manifest_artifact.metadata["content_type"] == "application/json"
    assert manifest_artifact.metadata["runtime_id"] == "RUNTIME-0001"
    assert manifest_artifact.metadata["path"] == str(manifest_path.resolve())
    assert manifest["runtime_evidence"] == {
        "runtime_id": "RUNTIME-0001",
        "runtime_report_artifact_id": "ARTIFACT-0001",
        "trace_report_artifact_id": "ARTIFACT-0002",
        "artifact_count": 2,
    }
    assert [artifact["metadata"]["artifact_role"] for artifact in manifest["artifacts"]] == [
        "runtime_report",
        "runtime_trace_report",
    ]
    assert [artifact.id for artifact in store.list()] == ["ARTIFACT-0001", "ARTIFACT-0002", "ARTIFACT-0003"]


def test_runtime_evidence_bundle_writer_accepts_serialized_result_and_custom_manifest_path(tmp_path) -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [{"id": "NODE-0001", "plugin": "blender", "action": "render"}],
    }
    result = RuntimeEngine().run(specification, [WorkerCapability("WORKER-0001", ["generic"])])
    writer = RuntimeEvidenceBundleWriter(ArtifactStore(tmp_path))

    manifest_artifact = writer.write_evidence(result.to_dict(), relative_path="custom/evidence.json")
    manifest_path = tmp_path / "custom" / "evidence.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert result.status == RuntimeState.PARTIAL
    assert manifest_artifact.uri == manifest_path.resolve().as_uri()
    assert manifest_artifact.metadata["runtime_report_uri"].endswith("/reports/RUNTIME-0001.json")
    assert manifest_artifact.metadata["trace_report_uri"].endswith("/traces/RUNTIME-0001.json")
    assert manifest["runtime_evidence"]["runtime_id"] == "RUNTIME-0001"
    assert manifest["artifacts"][0]["metadata"]["runtime_status"] == "partial"
    assert manifest["artifacts"][1]["metadata"]["trace_status"] == "partial"


def test_runtime_evidence_manifest_verifier_accepts_written_manifest_artifact(tmp_path) -> None:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [{"id": "NODE-0001", "plugin": "generic", "action": "prepare"}],
    }
    result = RuntimeEngine().run(specification, [WorkerCapability("WORKER-0001", ["generic"])])
    manifest_artifact = RuntimeEvidenceBundleWriter(ArtifactStore(tmp_path)).write_evidence(result)

    verification = verify_runtime_evidence_manifest(manifest_artifact)

    assert verification.successful() is True
    assert verification.to_dict() == {
        "runtime_evidence_verification": {"successful": True, "issue_count": 0},
        "issues": [],
    }


def test_runtime_evidence_manifest_verifier_reports_manifest_mismatches() -> None:
    verification = verify_runtime_evidence_manifest(
        {
            "runtime_evidence": {
                "runtime_id": "RUNTIME-0001",
                "runtime_report_artifact_id": "ARTIFACT-OTHER",
                "trace_report_artifact_id": "ARTIFACT-0002",
                "artifact_count": 1,
            },
            "artifacts": [
                {
                    "id": "ARTIFACT-0001",
                    "uri": "file:///runtime.json",
                    "metadata": {"artifact_role": "runtime_trace_report", "runtime_id": "RUNTIME-0001"},
                },
                {
                    "id": "ARTIFACT-0002",
                    "metadata": {"artifact_role": "runtime_report", "runtime_id": "RUNTIME-OTHER"},
                },
            ],
        }
    )

    assert verification.successful() is False
    assert verification.issues == [
        "Runtime evidence artifact_count must match artifacts length.",
        "Runtime evidence artifacts must include runtime_report then runtime_trace_report.",
        "Runtime evidence runtime_report_artifact_id must match runtime report artifact id.",
        "Runtime evidence artifact 2 runtime_id must match evidence runtime_id.",
        "Runtime evidence artifact 2 requires uri.",
    ]
