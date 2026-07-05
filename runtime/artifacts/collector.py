from __future__ import annotations

from typing import Any

from runtime.artifacts.models import RuntimeArtifact
from runtime.artifacts.store import ArtifactStore
from runtime.execution.models import ExecutionResult


class ArtifactCollector:
    """Collects runtime execution outputs into an artifact store."""

    def __init__(self, store: ArtifactStore | None = None) -> None:
        self.store = store or ArtifactStore()

    def collect_from_execution(self, execution: ExecutionResult | dict[str, Any]) -> list[RuntimeArtifact]:
        execution_data = execution.to_dict() if isinstance(execution, ExecutionResult) else execution
        artifacts: list[RuntimeArtifact] = []
        for node_result in execution_data.get("node_results", []):
            if not isinstance(node_result, dict):
                continue
            artifacts.extend(self._collect_node_outputs(node_result))
        return artifacts

    def _collect_node_outputs(self, node_result: dict[str, Any]) -> list[RuntimeArtifact]:
        outputs = node_result.get("outputs", [])
        if not isinstance(outputs, list):
            return []

        artifacts: list[RuntimeArtifact] = []
        producer = str(node_result.get("node_id", "UNKNOWN-NODE"))
        for index, output in enumerate(outputs, start=1):
            if not isinstance(output, str) or not output:
                continue
            artifacts.append(
                self.store.record_uri(
                    output,
                    producer=producer,
                    metadata={
                        "output_index": index,
                        "worker_id": str(node_result.get("worker_id", "UNKNOWN-WORKER")),
                        "plugin": str(node_result.get("plugin", "unknown")),
                        "action": str(node_result.get("action", "unknown")),
                        "status": str(node_result.get("status", "unknown")),
                    },
                )
            )
        return artifacts
