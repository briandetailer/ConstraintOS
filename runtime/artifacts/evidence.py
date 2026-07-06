from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime.artifacts.models import RuntimeArtifact
from runtime.artifacts.reporter import RuntimeReportWriter
from runtime.artifacts.store import ArtifactStore
from runtime.artifacts.trace_reporter import RuntimeTraceReportWriter
from runtime.result import RuntimeResult


class RuntimeEvidenceBundleWriter:
    """Writes runtime report, trace report, and a manifest linking both artifacts."""

    def __init__(self, store: ArtifactStore | None = None) -> None:
        self.store = store or ArtifactStore()
        self.runtime_reports = RuntimeReportWriter(self.store)
        self.trace_reports = RuntimeTraceReportWriter(self.store)

    def write_evidence(
        self,
        result: RuntimeResult | dict[str, Any],
        relative_path: str | Path | None = None,
    ) -> RuntimeArtifact:
        result_data = result.to_dict() if isinstance(result, RuntimeResult) else result
        if not isinstance(result_data, dict):
            result_data = {}
        runtime_id = self._runtime_id(result_data)
        runtime_report = self.runtime_reports.write_report(result_data)
        trace_report = self.trace_reports.write_trace(result_data)
        manifest = {
            "runtime_evidence": {
                "runtime_id": runtime_id,
                "runtime_report_artifact_id": runtime_report.id,
                "trace_report_artifact_id": trace_report.id,
                "artifact_count": 2,
            },
            "artifacts": [runtime_report.to_dict(), trace_report.to_dict()],
        }
        manifest_path = relative_path or f"evidence/{runtime_id}.json"
        content = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        return self.store.write_text(
            manifest_path,
            content,
            producer=runtime_id,
            metadata={
                "artifact_role": "runtime_evidence_manifest",
                "content_type": "application/json",
                "runtime_id": runtime_id,
                "runtime_report_uri": runtime_report.uri,
                "trace_report_uri": trace_report.uri,
            },
        )

    def _runtime_id(self, result_data: dict[str, Any]) -> str:
        runtime_result = result_data.get("runtime_result", {})
        if not isinstance(runtime_result, dict):
            runtime_result = {}
        return str(runtime_result.get("id", "RUNTIME-UNKNOWN"))
