from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class EnvironmentProfile:
    id: str
    name: str
    mode: str
    description: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "environment_profile": {
                "id": self.id,
                "name": self.name,
                "mode": self.mode,
                "description": self.description,
                "created": date.today().isoformat(),
            }
        }


@dataclass
class RuntimeLimits:
    id: str
    max_concurrent_jobs: int = 1
    max_payload_bytes: int = 1048576
    max_retries: int = 3
    allow_live_renderers: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "runtime_limits": {
                "id": self.id,
                "max_concurrent_jobs": self.max_concurrent_jobs,
                "max_payload_bytes": self.max_payload_bytes,
                "max_retries": self.max_retries,
                "allow_live_renderers": self.allow_live_renderers,
                "created": date.today().isoformat(),
            }
        }


@dataclass
class FeatureFlags:
    id: str
    flags: dict[str, bool]

    def to_dict(self) -> dict[str, Any]:
        return {
            "feature_flags": {
                "id": self.id,
                "created": date.today().isoformat(),
            },
            "flags": self.flags,
        }


def create_development_profile() -> dict[str, Any]:
    return EnvironmentProfile("ENV-0001", "development", "development", "Local development profile with dry-run execution defaults.").to_dict()


def create_production_profile() -> dict[str, Any]:
    return EnvironmentProfile("ENV-0002", "production", "production", "Production profile requiring explicit safety gates and durable runtime services.").to_dict()


def validate_runtime_safety(profile: dict[str, Any], limits: dict[str, Any], flags: dict[str, Any]) -> dict[str, Any]:
    profile_data = profile.get("environment_profile", profile)
    limits_data = limits.get("runtime_limits", limits)
    flag_values = flags.get("flags", flags)
    findings: list[str] = []
    mode = profile_data.get("mode", "development")
    if mode == "production" and limits_data.get("allow_live_renderers") is True:
        findings.append("Production live renderers require an explicit renderer safety gate.")
    if mode == "production" and flag_values.get("debug_mode") is True:
        findings.append("Debug mode must be disabled in production.")
    if limits_data.get("max_concurrent_jobs", 1) < 1:
        findings.append("max_concurrent_jobs must be at least 1.")
    return {
        "runtime_safety_check": {
            "status": "pass" if not findings else "fail",
            "created": date.today().isoformat(),
        },
        "findings": findings,
    }
