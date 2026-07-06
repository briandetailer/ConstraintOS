from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

PASSING_EVIDENCE_STATUSES = frozenset({"pass", "passed", "complete", "approved"})
FAILING_EVIDENCE_STATUSES = frozenset({"fail", "failed", "rejected"})
ALLOWED_EVIDENCE_STATUSES = PASSING_EVIDENCE_STATUSES | FAILING_EVIDENCE_STATUSES


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

    def __post_init__(self) -> None:
        normalized = self.status.lower().strip()
        if normalized not in ALLOWED_EVIDENCE_STATUSES:
            allowed = ", ".join(sorted(ALLOWED_EVIDENCE_STATUSES))
            raise ValueError(f"validation evidence status is not registered: {self.status}. Expected one of: {allowed}")
        object.__setattr__(self, "status", normalized)

    def passed(self) -> bool:
        return self.status in PASSING_EVIDENCE_STATUSES

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
