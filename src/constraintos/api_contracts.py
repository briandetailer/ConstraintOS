from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class ApiEndpoint:
    method: str
    path: str
    operation_id: str
    summary: str
    request_schema: str | None = None
    response_schema: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "method": self.method,
            "path": self.path,
            "operation_id": self.operation_id,
            "summary": self.summary,
            "request_schema": self.request_schema,
            "response_schema": self.response_schema,
        }


def create_api_catalog() -> dict[str, Any]:
    endpoints = [
        ApiEndpoint("GET", "/health", "get_health", "Return runtime health."),
        ApiEndpoint("POST", "/compile", "compile_specification", "Compile a CSL specification into instructions.", "csl.schema.json", "compiler-result.schema.json"),
        ApiEndpoint("POST", "/validate", "validate_artifact", "Validate an artifact or record.", null_schema(), "compliance-report.schema.json"),
        ApiEndpoint("POST", "/render-jobs", "create_render_job", "Create a render job.", "render-job.schema.json", "render-job.schema.json"),
        ApiEndpoint("POST", "/builds/volume", "create_volume_build", "Run or queue a volume build.", "volume-plan.schema.json", "volume-build.schema.json"),
        ApiEndpoint("GET", "/jobs/{job_id}", "get_runtime_job", "Return runtime job status.", None, "runtime-job.schema.json"),
    ]
    return {
        "api_catalog": {
            "id": "API-CATALOG-0001",
            "created": date.today().isoformat(),
            "version": "1.0.0-alpha.14",
            "status": "draft",
        },
        "endpoints": [endpoint.to_dict() for endpoint in endpoints],
    }


def null_schema() -> str:
    return "kernel-validation-request.schema.json"


def create_api_error(error_id: str, code: str, message: str, retryable: bool = False) -> dict[str, Any]:
    return {
        "api_error": {
            "id": error_id,
            "code": code,
            "message": message,
            "retryable": retryable,
            "created": date.today().isoformat(),
        }
    }


def create_service_boundary(service_id: str, name: str, owns: list[str], does_not_own: list[str]) -> dict[str, Any]:
    return {
        "service_boundary": {
            "id": service_id,
            "name": name,
            "created": date.today().isoformat(),
        },
        "owns": owns,
        "does_not_own": does_not_own,
    }
