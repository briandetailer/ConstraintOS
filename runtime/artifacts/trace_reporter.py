from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime.artifacts.models import RuntimeArtifact
from runtime.artifacts.store import ArtifactStore
from runtime.result import RuntimeResult
from runtime.traceability import RuntimeTrace, runtime_result_to_trace, verify_runtime_trace


class RuntimeTraceReportWriter:
    """Writes runtime traceability snapshots as JSON artifacts."""

    def __init__(self, store: ArtifactStore | None = None) -> None:
        self.store = store or ArtifactStore()

    def write_trace(
        self,
        trace: RuntimeTrace | RuntimeResult | dict[str, Any],
        relative_path: str | Path | None = None,
    ) -> RuntimeArtifact:
        trace_data = self._trace_data(trace)
        verification = verify_runtime_trace(trace_data)
        if not verification.successful():
            raise ValueError("Runtime trace report requires a valid runtime trace.")

        trace_header = trace_data["runtime_traceability"]
        runtime_id = str(trace_header["runtime_id"])
        report_path = relative_path or f"traces/{runtime_id}.json"
        content = json.dumps(trace_data, indent=2, sort_keys=True) + "\n"
        return self.store.write_text(
            report_path,
            content,
            producer=runtime_id,
            metadata={
                "artifact_role": "runtime_trace_report",
                "content_type": "application/json",
                "runtime_id": runtime_id,
                "trace_status": trace_header.get("status", "unknown"),
                "trace_success": trace_header.get("success", False),
                "record_count": trace_header.get("record_count", 0),
            },
        )

    def _trace_data(self, trace: RuntimeTrace | RuntimeResult | dict[str, Any]) -> dict[str, Any]:
        if isinstance(trace, RuntimeTrace):
            return trace.to_dict()
        if isinstance(trace, RuntimeResult):
            return runtime_result_to_trace(trace).to_dict()
        if isinstance(trace, dict) and "runtime_result" in trace:
            return runtime_result_to_trace(trace).to_dict()
        return trace if isinstance(trace, dict) else {}
