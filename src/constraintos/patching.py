from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class FailedConstraint:
    constraint_id: str
    severity: str
    result: str
    evidence: str = ""
    recommended_fix: str = ""


@dataclass
class PatchPackage:
    patch_id: str
    artifact_id: str
    source_report_id: str
    failed_constraints: list[FailedConstraint]
    instruction: str
    created: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "patch": {
                "id": self.patch_id,
                "artifact_id": self.artifact_id,
                "source_report_id": self.source_report_id,
                "created": self.created,
                "status": "draft",
            },
            "failed_constraints": [constraint.__dict__ for constraint in self.failed_constraints],
            "instruction": self.instruction,
        }


def build_patch_instruction(report: dict[str, Any]) -> str:
    artifact = report.get("artifact", {})
    results = report.get("constraint_results", []) or []
    failed = [item for item in results if item.get("result") in {"fail", "uncertain", "blocked_by_missing_evidence"}]

    lines = [
        f"Patch artifact {artifact.get('id', 'UNKNOWN')} only for the failed or uncertain constraints below.",
        "Do not alter passing constraints or unrelated regions.",
        "Preserve all previously approved geometry and style unless directly contradicted by the failed constraint.",
        "",
        "FAILED OR UNCERTAIN CONSTRAINTS",
    ]
    for item in failed:
        lines.append(f"- {item.get('constraint_id')}: {item.get('result')} ({item.get('severity')})")
        if item.get("evidence"):
            lines.append(f"  evidence: {item.get('evidence')}")
        if item.get("recommended_fix"):
            lines.append(f"  recommended fix: {item.get('recommended_fix')}")
    if not failed:
        lines.append("- None. No patch required.")
    return "\n".join(lines)


def create_patch_package(report: dict[str, Any], patch_id: str) -> PatchPackage:
    failed: list[FailedConstraint] = []
    for item in report.get("constraint_results", []) or []:
        if item.get("result") in {"fail", "uncertain", "blocked_by_missing_evidence"}:
            failed.append(
                FailedConstraint(
                    constraint_id=str(item.get("constraint_id", "UNKNOWN")),
                    severity=str(item.get("severity", "major")),
                    result=str(item.get("result", "uncertain")),
                    evidence=str(item.get("evidence", "")),
                    recommended_fix=str(item.get("recommended_fix", "")),
                )
            )
    return PatchPackage(
        patch_id=patch_id,
        artifact_id=str(report.get("artifact", {}).get("id", "UNKNOWN")),
        source_report_id=str(report.get("report", {}).get("id", "UNKNOWN")),
        failed_constraints=failed,
        instruction=build_patch_instruction(report),
        created=date.today().isoformat(),
    )


def create_regression_baseline(artifact_id: str, artifact_version: str, approved_report_id: str, approved_constraints: list[str]) -> dict[str, Any]:
    return {
        "baseline": {
            "artifact_id": artifact_id,
            "artifact_version": artifact_version,
            "approved_report_id": approved_report_id,
            "created": date.today().isoformat(),
            "status": "active",
        },
        "approved_constraints": approved_constraints,
        "regression_policy": {
            "blocker_regression_allowed": False,
            "major_regression_allowed": False,
            "minor_regression_requires_note": True,
        },
    }
