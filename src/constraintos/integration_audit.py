from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


PHASE_20_22_SCHEMA_KEYS: dict[str, str] = {
    "runtime_health_report": "schemas/runtime-health-report.schema.json",
    "worker_fleet_status": "schemas/worker-fleet-status.schema.json",
    "job_queue_summary": "schemas/job-queue-summary.schema.json",
    "failure_summary_report": "schemas/failure-summary-report.schema.json",
    "environment_profile": "schemas/environment-profile.schema.json",
    "runtime_limits": "schemas/runtime-limits.schema.json",
    "feature_flags": "schemas/feature-flags.schema.json",
    "runtime_safety_check": "schemas/runtime-safety-check.schema.json",
    "local_runtime_profile": "schemas/local-runtime-profile.schema.json",
    "runtime_command": "schemas/runtime-command.schema.json",
    "local_deployment_checklist": "schemas/local-deployment-checklist.schema.json",
}


@dataclass
class IntegrationAuditResult:
    id: str
    status: str
    checked: int
    missing: list[str]
    notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "integration_audit": {
                "id": self.id,
                "status": self.status,
                "checked": self.checked,
                "created": date.today().isoformat(),
            },
            "missing": self.missing,
            "notes": self.notes,
        }


def detect_integration_schema(data: dict[str, Any]) -> str | None:
    for key, schema_path in PHASE_20_22_SCHEMA_KEYS.items():
        if key in data:
            return schema_path
    return None


def audit_schema_files(repo_root: str | Path = ".") -> IntegrationAuditResult:
    root = Path(repo_root)
    missing = [schema for schema in PHASE_20_22_SCHEMA_KEYS.values() if not (root / schema).exists()]
    return IntegrationAuditResult(
        id="AUDIT-0001",
        status="pass" if not missing else "fail",
        checked=len(PHASE_20_22_SCHEMA_KEYS),
        missing=missing,
        notes=["Phase 20-22 schema coverage audit."],
    )


def audit_example_detection(examples: list[dict[str, Any]]) -> IntegrationAuditResult:
    missing: list[str] = []
    for index, example in enumerate(examples, start=1):
        if detect_integration_schema(example) is None:
            missing.append(f"example-{index}")
    return IntegrationAuditResult(
        id="AUDIT-0002",
        status="pass" if not missing else "fail",
        checked=len(examples),
        missing=missing,
        notes=["Phase 20-22 example schema detection audit."],
    )


def create_ci_readiness_report(schema_audit: dict[str, Any], example_audit: dict[str, Any]) -> dict[str, Any]:
    schema_status = schema_audit.get("integration_audit", {}).get("status", "unknown")
    example_status = example_audit.get("integration_audit", {}).get("status", "unknown")
    status = "ready" if schema_status == "pass" and example_status == "pass" else "blocked"
    return {
        "ci_readiness_report": {
            "id": "CI-READY-0001",
            "status": status,
            "created": date.today().isoformat(),
        },
        "schema_audit_status": schema_status,
        "example_audit_status": example_status,
        "recommendation": "run_ci" if status == "ready" else "resolve_audit_failures",
    }
