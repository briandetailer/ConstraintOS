from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class LocalRuntimeProfile:
    id: str
    name: str
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    worker_enabled: bool = False
    storage_root: str = "artifact_store"

    def to_dict(self) -> dict[str, Any]:
        return {
            "local_runtime_profile": {
                "id": self.id,
                "name": self.name,
                "api_host": self.api_host,
                "api_port": self.api_port,
                "worker_enabled": self.worker_enabled,
                "storage_root": self.storage_root,
                "created": date.today().isoformat(),
            }
        }


@dataclass
class RuntimeCommand:
    id: str
    name: str
    command: str
    purpose: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "runtime_command": {
                "id": self.id,
                "name": self.name,
                "command": self.command,
                "purpose": self.purpose,
                "created": date.today().isoformat(),
            }
        }


def create_local_runtime_profile() -> dict[str, Any]:
    return LocalRuntimeProfile("LOCAL-0001", "local-development").to_dict()


def create_api_run_command() -> dict[str, Any]:
    return RuntimeCommand(
        "COMMAND-0001",
        "run-api",
        "uvicorn constraintos.api_server:app --host 127.0.0.1 --port 8000",
        "Run the local ConstraintOS API server.",
    ).to_dict()


def create_worker_run_command() -> dict[str, Any]:
    return RuntimeCommand(
        "COMMAND-0002",
        "run-worker-dry",
        "python -m constraintos.worker",
        "Reserved local worker launch command for future worker runner implementation.",
    ).to_dict()


def create_local_deployment_checklist(checklist_id: str = "DEPLOY-0001") -> dict[str, Any]:
    return {
        "local_deployment_checklist": {
            "id": checklist_id,
            "created": date.today().isoformat(),
            "status": "draft",
        },
        "items": [
            {"id": "LD-001", "description": "Create virtual environment.", "required": True},
            {"id": "LD-002", "description": "Install package in editable mode.", "required": True},
            {"id": "LD-003", "description": "Run tests.", "required": True},
            {"id": "LD-004", "description": "Run API server locally.", "required": True},
            {"id": "LD-005", "description": "Verify /health endpoint.", "required": True},
        ],
    }
