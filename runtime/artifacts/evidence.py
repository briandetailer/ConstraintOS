from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from runtime.artifacts.contract_reporter import RuntimeContractRegistryReportWriter
from runtime.artifacts.models import RuntimeArtifact
from runtime.artifacts.reporter import RuntimeReportWriter
from runtime.artifacts.store import ArtifactStore
from runtime.artifacts.trace_reporter import RuntimeTraceReportWriter
from runtime.contracts import CONTRACT_REGISTRY_VERSION
from runtime.result import RuntimeResult


@dataclass(frozen=True)
class RuntimeEvidenceVerification:
    issues: list[str] = field(default_factory=list)

    def successful(self) -> bool:
        return not self.issues

    def to_dict(self) -> dict[str, Any]:
        return {
            "runtime_evidence_verification": {
                "successful": self.successful(),
                "issue_count": len(self.issues),
            },
            "issues": self.issues,
        }


class RuntimeEvidenceBundleWriter:
    """Writes runtime report, trace report, contract registry, and an evidence manifest."""

    def __init__(self, store: ArtifactStore | None = None) -> None:
        self.store = store or ArtifactStore()
        self.runtime_reports = RuntimeReportWriter(self.store)
        self.trace_reports = RuntimeTraceReportWriter(self.store)
        self.contract_registries = RuntimeContractRegistryReportWriter(self.store)

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
        contract_registry = self.contract_registries.write_registry()
        manifest = {
            "runtime_evidence": {
                "runtime_id": runtime_id,
                "contract_registry_version": CONTRACT_REGISTRY_VERSION,
                "runtime_report_artifact_id": runtime_report.id,
                "trace_report_artifact_id": trace_report.id,
                "contract_registry_artifact_id": contract_registry.id,
                "artifact_count": 3,
            },
            "artifacts": [runtime_report.to_dict(), trace_report.to_dict(), contract_registry.to_dict()],
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
                "contract_registry_version": CONTRACT_REGISTRY_VERSION,
                "runtime_report_uri": runtime_report.uri,
                "trace_report_uri": trace_report.uri,
                "contract_registry_uri": contract_registry.uri,
            },
        )

    def _runtime_id(self, result_data: dict[str, Any]) -> str:
        runtime_result = result_data.get("runtime_result", {})
        if not isinstance(runtime_result, dict):
            runtime_result = {}
        return str(runtime_result.get("id", "RUNTIME-UNKNOWN"))


def verify_runtime_evidence_manifest(manifest: RuntimeArtifact | dict[str, Any]) -> RuntimeEvidenceVerification:
    manifest_data = manifest.to_dict() if isinstance(manifest, RuntimeArtifact) else manifest
    issues: list[str] = []

    if not isinstance(manifest_data, dict):
        return RuntimeEvidenceVerification(["Runtime evidence manifest must be a dictionary or RuntimeArtifact."])

    if "runtime_evidence" not in manifest_data and "metadata" in manifest_data:
        path = _metadata(manifest_data).get("path")
        if isinstance(path, str) and path:
            try:
                manifest_data = json.loads(Path(path).read_text(encoding="utf-8"))
            except OSError:
                return RuntimeEvidenceVerification(["Runtime evidence manifest artifact path must be readable."])
            except json.JSONDecodeError:
                return RuntimeEvidenceVerification(["Runtime evidence manifest artifact content must be valid JSON."])

    evidence = _dict_value(manifest_data, "runtime_evidence")
    artifacts = manifest_data.get("artifacts", [])
    runtime_id = str(evidence.get("runtime_id", ""))

    if not runtime_id:
        issues.append("Runtime evidence runtime_id is required.")
    if evidence.get("contract_registry_version") != CONTRACT_REGISTRY_VERSION:
        issues.append(f"Runtime evidence contract_registry_version must be {CONTRACT_REGISTRY_VERSION}.")
    if not isinstance(evidence.get("artifact_count"), int):
        issues.append("Runtime evidence artifact_count must be an integer.")
    elif isinstance(artifacts, list) and evidence.get("artifact_count") != len(artifacts):
        issues.append("Runtime evidence artifact_count must match artifacts length.")
    if not isinstance(artifacts, list):
        issues.append("Runtime evidence artifacts must be a list.")
        return RuntimeEvidenceVerification(issues)

    roles = [_metadata(artifact).get("artifact_role") for artifact in artifacts if isinstance(artifact, dict)]
    expected_roles = ["runtime_report", "runtime_trace_report", "runtime_contract_registry"]
    if roles != expected_roles:
        issues.append("Runtime evidence artifacts must include runtime_report, runtime_trace_report, then runtime_contract_registry.")

    report_artifact = artifacts[0] if len(artifacts) > 0 and isinstance(artifacts[0], dict) else {}
    trace_artifact = artifacts[1] if len(artifacts) > 1 and isinstance(artifacts[1], dict) else {}
    registry_artifact = artifacts[2] if len(artifacts) > 2 and isinstance(artifacts[2], dict) else {}
    if report_artifact.get("id") != evidence.get("runtime_report_artifact_id"):
        issues.append("Runtime evidence runtime_report_artifact_id must match runtime report artifact id.")
    if trace_artifact.get("id") != evidence.get("trace_report_artifact_id"):
        issues.append("Runtime evidence trace_report_artifact_id must match trace report artifact id.")
    if registry_artifact.get("id") != evidence.get("contract_registry_artifact_id"):
        issues.append("Runtime evidence contract_registry_artifact_id must match contract registry artifact id.")

    for index, artifact in enumerate(artifacts, start=1):
        if not isinstance(artifact, dict):
            issues.append(f"Runtime evidence artifact {index} must be a dictionary.")
            continue
        metadata = _metadata(artifact)
        role = metadata.get("artifact_role")
        if runtime_id and role != "runtime_contract_registry" and metadata.get("runtime_id") != runtime_id:
            issues.append(f"Runtime evidence artifact {index} runtime_id must match evidence runtime_id.")
        if role == "runtime_contract_registry" and metadata.get("registry_version") != CONTRACT_REGISTRY_VERSION:
            issues.append(f"Runtime evidence artifact {index} registry_version must match contract registry version.")
        if not artifact.get("uri"):
            issues.append(f"Runtime evidence artifact {index} requires uri.")

    return RuntimeEvidenceVerification(issues)


def _dict_value(value: dict[str, Any], key: str) -> dict[str, Any]:
    payload = value.get(key, {}) if isinstance(value, dict) else {}
    return payload if isinstance(payload, dict) else {}


def _metadata(value: dict[str, Any]) -> dict[str, Any]:
    metadata = value.get("metadata", {}) if isinstance(value, dict) else {}
    return metadata if isinstance(metadata, dict) else {}
