from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime.artifacts.models import RuntimeArtifact
from runtime.artifacts.store import ArtifactStore
from runtime.result import RuntimeResult


class RuntimeReportWriter:
    """Writes runtime result snapshots as JSON artifacts."""

    def __init__(self, store: ArtifactStore | None = None) -> None:
        self.store = store or ArtifactStore()

    def write_report(
        self,
        result: RuntimeResult | dict[str, Any],
        relative_path: str | Path | None = None,
    ) -> RuntimeArtifact:
        result_data = result.to_dict() if isinstance(result, RuntimeResult) else result
        runtime_id = self._runtime_id(result_data)
        report_path = relative_path or f"reports/{runtime_id}.json"
        content = json.dumps(result_data, indent=2, sort_keys=True) + "\n"
        return self.store.write_text(
            report_path,
            content,
            producer=runtime_id,
            metadata={
                "content_type": "application/json",
                "runtime_id": runtime_id,
                "artifact_role": "runtime_report",
            },
        )

    def _runtime_id(self, result_data: dict[str, Any]) -> str:
        runtime_result = result_data.get("runtime_result", {})
        return str(runtime_result.get("id", "RUNTIME-UNKNOWN"))
