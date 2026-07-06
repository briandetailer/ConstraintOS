from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any


@dataclass(frozen=True)
class ValidationIssueCode:
    """Machine-readable validation issue reason."""

    code: str
    title: str
    severity: str
    remediation: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "title": self.title,
            "severity": self.severity,
            "remediation": self.remediation,
        }


@dataclass(frozen=True)
class ValidationGate:
    """A single validation gate that must be evaluated before approval."""

    id: str
    name: str
    required_pass: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "required_pass": self.required_pass,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class ValidationEvidence:
    """Evidence supplied to a validation gate."""

    gate_id: str
    status: str
    message: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    def passed(self) -> bool:
        return self.status.lower() in {"pass", "passed", "complete", "approved"}

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "status": self.status,
            "message": self.message,
            "details": self.details,
        }


@dataclass(frozen=True)
class ValidationResult:
    """Result for one evaluated validation gate."""

    gate_id: str
    name: str
    status: str
    required_pass: bool
    reason: str = ""
    evidence: dict[str, Any] | None = None
    issue_code: ValidationIssueCode | None = None

    def passed(self) -> bool:
        return self.status == "passed"

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "name": self.name,
            "status": self.status,
            "required_pass": self.required_pass,
            "reason": self.reason,
            "evidence": self.evidence,
            "issue_code": self.issue_code.to_dict() if self.issue_code else None,
        }


@dataclass(frozen=True)
class ValidationReport:
    """Structured report produced by the validation kernel."""

    id: str
    subject_id: str
    status: str
    results: list[ValidationResult]
    messages: list[str] = field(default_factory=list)
    constraint_packs: list[dict[str, Any]] = field(default_factory=list)

    def passed(self) -> bool:
        return self.status == "passed"

    def to_dict(self) -> dict[str, Any]:
        return {
            "validation_report": {
                "id": self.id,
                "subject_id": self.subject_id,
                "status": self.status,
                "created": date.today().isoformat(),
                "constraint_packs": self.constraint_packs,
            },
            "results": [result.to_dict() for result in self.results],
            "messages": self.messages,
        }
