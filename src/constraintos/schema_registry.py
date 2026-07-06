from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass(frozen=True)
class SchemaRegistration:
    key: str
    schema_path: str
    record_type: str


SCHEMA_REGISTRY: tuple[SchemaRegistration, ...] = (
    SchemaRegistration("failure", "schemas/failure.schema.json", "failure"),
    SchemaRegistration("registry", "schemas/id-registry.schema.json", "id_registry"),
    SchemaRegistration("patch", "schemas/patch-package.schema.json", "patch_package"),
    SchemaRegistration("baseline", "schemas/regression-baseline.schema.json", "regression_baseline"),
    SchemaRegistration("approval", "schemas/approval-record.schema.json", "approval_record"),
    SchemaRegistration("review_checklist", "schemas/review-checklist.schema.json", "review_checklist"),
    SchemaRegistration("build_plan", "schemas/build-plan.schema.json", "build_plan"),
    SchemaRegistration("render_job", "schemas/render-job.schema.json", "render_job"),
    SchemaRegistration("render_specification", "schemas/render-specification.schema.json", "render_specification"),
    SchemaRegistration("constraint_pack", "schemas/constraint-pack.schema.json", "constraint_pack"),
    SchemaRegistration("evidence", "schemas/validation-evidence.schema.json", "validation_evidence"),
    SchemaRegistration("output_reference", "schemas/output-reference.schema.json", "output_reference"),
    SchemaRegistration("renderer_registry", "schemas/renderer-registry.schema.json", "renderer_registry"),
    SchemaRegistration("stored_object", "schemas/stored-object.schema.json", "stored_object"),
    SchemaRegistration("storage_backend", "schemas/storage-backend.schema.json", "storage_backend"),
    SchemaRegistration("volume_plan", "schemas/volume-plan.schema.json", "volume_plan"),
    SchemaRegistration("volume_build", "schemas/volume-build.schema.json", "volume_build"),
    SchemaRegistration("volume_completion_report", "schemas/volume-completion-report.schema.json", "volume_completion_report"),
    SchemaRegistration("runtime_config", "schemas/runtime-config.schema.json", "runtime_config"),
    SchemaRegistration("runtime_job", "schemas/runtime-job.schema.json", "runtime_job"),
    SchemaRegistration("worker_profile", "schemas/worker-profile.schema.json", "worker_profile"),
    SchemaRegistration("worker_result", "schemas/worker-result.schema.json", "worker_result"),
    SchemaRegistration("worker_job_types", "schemas/worker-job-type.schema.json", "worker_job_type_registry"),
    SchemaRegistration("worker_heartbeat", "schemas/worker-heartbeat.schema.json", "worker_heartbeat"),
    SchemaRegistration("job_lease", "schemas/job-lease.schema.json", "job_lease"),
    SchemaRegistration("lease_decision", "schemas/lease-decision.schema.json", "lease_decision"),
    SchemaRegistration("metric_event", "schemas/metric-event.schema.json", "metric_event"),
    SchemaRegistration("api_catalog", "schemas/api-catalog.schema.json", "api_catalog"),
    SchemaRegistration("api_error", "schemas/api-error.schema.json", "api_error"),
    SchemaRegistration("service_boundary", "schemas/service-boundary.schema.json", "service_boundary"),
    SchemaRegistration("validation_request", "schemas/kernel-validation-request.schema.json", "validation_request"),
    SchemaRegistration("queue_record", "schemas/queue-record.schema.json", "queue_record"),
    SchemaRegistration("queue_status", "schemas/queue-status.schema.json", "queue_status"),
    SchemaRegistration("retry_policy", "schemas/retry-policy.schema.json", "retry_policy"),
    SchemaRegistration("retry_decision", "schemas/retry-decision.schema.json", "retry_decision"),
    SchemaRegistration("failed_job", "schemas/failed-job.schema.json", "failed_job"),
    SchemaRegistration("runtime_health_report", "schemas/runtime-health-report.schema.json", "runtime_health_report"),
    SchemaRegistration("worker_fleet_status", "schemas/worker-fleet-status.schema.json", "worker_fleet_status"),
    SchemaRegistration("job_queue_summary", "schemas/job-queue-summary.schema.json", "job_queue_summary"),
    SchemaRegistration("failure_summary_report", "schemas/failure-summary-report.schema.json", "failure_summary_report"),
    SchemaRegistration("environment_profile", "schemas/environment-profile.schema.json", "environment_profile"),
    SchemaRegistration("runtime_limits", "schemas/runtime-limits.schema.json", "runtime_limits"),
    SchemaRegistration("feature_flags", "schemas/feature-flags.schema.json", "feature_flags"),
    SchemaRegistration("runtime_safety_check", "schemas/runtime-safety-check.schema.json", "runtime_safety_check"),
    SchemaRegistration("local_runtime_profile", "schemas/local-runtime-profile.schema.json", "local_runtime_profile"),
    SchemaRegistration("runtime_command", "schemas/runtime-command.schema.json", "runtime_command"),
    SchemaRegistration("local_deployment_checklist", "schemas/local-deployment-checklist.schema.json", "local_deployment_checklist"),
    SchemaRegistration("integration_audit", "schemas/integration-audit.schema.json", "integration_audit"),
    SchemaRegistration("ci_readiness_report", "schemas/ci-readiness-report.schema.json", "ci_readiness_report"),
    SchemaRegistration("schema_registry_report", "schemas/schema-registry-report.schema.json", "schema_registry_report"),
    SchemaRegistration("id_audit_report", "schemas/id-audit-report.schema.json", "id_audit_report"),
    SchemaRegistration("repository_health_summary", "schemas/repository-health-summary.schema.json", "repository_health_summary"),
    SchemaRegistration("repository_inventory", "schemas/repository-inventory.schema.json", "repository_inventory"),
    SchemaRegistration("repository_audit", "schemas/repository-audit.schema.json", "repository_audit"),
)

SPECIAL_SCHEMA_RULES: tuple[tuple[tuple[str, ...], str, str], ...] = (
    (("status", "service", "version"), "schemas/api-health.schema.json", "api_health_response"),
    (("status", "message", "request", "repo_root"), "schemas/api-validation-stub-response.schema.json", "api_validation_stub_response"),
    (("report", "constraint_results"), "schemas/compliance-report.schema.json", "compliance_report"),
    (("manifest", "history"), "schemas/artifact-manifest.schema.json", "artifact_manifest"),
    (("gate", "blocked_items"), "schemas/review-gate.schema.json", "review_gate"),
    (("iteration", "stage", "artifact_id"), "schemas/iteration-record.schema.json", "iteration_record"),
    (("name", "supported_constraint_types"), "schemas/renderer-profile.schema.json", "renderer_profile"),
    (("renderer", "instruction", "unsupported_constraints"), "schemas/compiler-result.schema.json", "compiler_result"),
    (("artifact", "constraints", "validation"), "schemas/csl.schema.json", "csl_artifact"),
)


def detect_schema(data: dict[str, Any]) -> str | None:
    for registration in SCHEMA_REGISTRY:
        if registration.key in data:
            return registration.schema_path
    for required_keys, schema_path, _record_type in SPECIAL_SCHEMA_RULES:
        if all(key in data for key in required_keys):
            return schema_path
    return None


def detect_record_type(data: dict[str, Any]) -> str | None:
    for registration in SCHEMA_REGISTRY:
        if registration.key in data:
            return registration.record_type
    for required_keys, _schema_path, record_type in SPECIAL_SCHEMA_RULES:
        if all(key in data for key in required_keys):
            return record_type
    return None


def registry_report() -> dict[str, Any]:
    return {
        "schema_registry_report": {
            "id": "SCHEMA-REGISTRY-0001",
            "created": date.today().isoformat(),
            "registered": len(SCHEMA_REGISTRY),
            "special_rules": len(SPECIAL_SCHEMA_RULES),
        },
        "schemas": [registration.__dict__ for registration in SCHEMA_REGISTRY],
    }
