from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from constraintos.job_queue import QueueRecord


@dataclass
class RetryPolicy:
    id: str
    max_attempts: int = 3
    retryable_statuses: list[str] | None = None
    backoff_strategy: str = "linear"

    def to_dict(self) -> dict[str, Any]:
        return {
            "retry_policy": {
                "id": self.id,
                "max_attempts": self.max_attempts,
                "retryable_statuses": self.retryable_statuses or ["failed", "blocked"],
                "backoff_strategy": self.backoff_strategy,
                "created": date.today().isoformat(),
            }
        }


@dataclass
class RetryDecision:
    job_id: str
    decision: str
    reason: str
    next_attempt: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "retry_decision": {
                "job_id": self.job_id,
                "decision": self.decision,
                "reason": self.reason,
                "next_attempt": self.next_attempt,
                "created": date.today().isoformat(),
            }
        }


@dataclass
class FailedJobRecord:
    id: str
    job_id: str
    job_type: str
    failure_class: str
    message: str
    attempt: int
    payload: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "failed_job": {
                "id": self.id,
                "job_id": self.job_id,
                "job_type": self.job_type,
                "failure_class": self.failure_class,
                "message": self.message,
                "attempt": self.attempt,
                "created": date.today().isoformat(),
            },
            "payload": self.payload,
        }


def classify_failure(message: str) -> str:
    lowered = message.lower()
    if "unsupported job type" in lowered:
        return "unsupported_job_type"
    if "missing" in lowered:
        return "missing_input"
    if "schema" in lowered or "validation" in lowered:
        return "validation_failure"
    return "runtime_failure"


def decide_retry(record: QueueRecord, attempt: int, policy: RetryPolicy, failure_message: str = "") -> RetryDecision:
    retryable_statuses = policy.retryable_statuses or ["failed", "blocked"]
    if record.status not in retryable_statuses:
        return RetryDecision(record.id, "do_not_retry", f"Status is not retryable: {record.status}", attempt)
    if classify_failure(failure_message) == "unsupported_job_type":
        return RetryDecision(record.id, "do_not_retry", "Unsupported job type requires configuration change.", attempt)
    if attempt >= policy.max_attempts:
        return RetryDecision(record.id, "send_to_failed_jobs", "Maximum attempts reached.", attempt)
    return RetryDecision(record.id, "retry", "Retry allowed by policy.", attempt + 1)


def create_failed_job(record: QueueRecord, failure_message: str, attempt: int) -> FailedJobRecord:
    return FailedJobRecord(
        id=f"FAILED-{record.id}",
        job_id=record.id,
        job_type=record.job_type,
        failure_class=classify_failure(failure_message),
        message=failure_message,
        attempt=attempt,
        payload=record.payload,
    )
