from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime.approval import verify_runtime_approval_decision
from runtime.artifacts.models import RuntimeArtifact
from runtime.artifacts.store import ArtifactStore


class RuntimeApprovalReportWriter:
    """Writes verified runtime approval decisions as JSON artifacts."""

    def __init__(self, store: ArtifactStore | None = None) -> None:
        self.store = store or ArtifactStore()

    def write_approval(
        self,
        decision: dict[str, Any],
        relative_path: str | Path | None = None,
    ) -> RuntimeArtifact:
        verification = verify_runtime_approval_decision(decision)
        if not verification.successful():
            raise ValueError("Runtime approval report requires a valid approval decision.")

        approval = decision["runtime_approval"]
        runtime_id = str(approval["runtime_id"])
        evidence_manifest_artifact_id = str(approval["evidence_manifest_artifact_id"])
        report_path = relative_path or f"approvals/{runtime_id}.json"
        content = json.dumps(decision, indent=2, sort_keys=True) + "\n"
        return self.store.write_text(
            report_path,
            content,
            producer=str(approval["decided_by"]),
            metadata={
                "artifact_role": "runtime_approval_report",
                "content_type": "application/json",
                "runtime_id": runtime_id,
                "evidence_manifest_artifact_id": evidence_manifest_artifact_id,
                "decision": approval["decision"],
                "approval_policy": approval["approval_policy"],
                "decided_by": approval["decided_by"],
                "decided_at": approval["decided_at"],
            },
        )
