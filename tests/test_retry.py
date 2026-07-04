from constraintos.job_queue import QueueRecord
from constraintos.retry import RetryPolicy, classify_failure, create_failed_job, decide_retry


def test_classify_failure() -> None:
    assert classify_failure("Unsupported job type: example") == "unsupported_job_type"
    assert classify_failure("missing specification") == "missing_input"
    assert classify_failure("schema validation failed") == "validation_failure"
    assert classify_failure("boom") == "runtime_failure"


def test_decide_retry_allowed() -> None:
    record = QueueRecord("JOB-0001", "volume_build", {}, status="failed")
    decision = decide_retry(record, attempt=1, policy=RetryPolicy("RETRY-0001", max_attempts=3), failure_message="temporary failure")
    assert decision.decision == "retry"
    assert decision.next_attempt == 2


def test_decide_retry_max_attempts() -> None:
    record = QueueRecord("JOB-0001", "volume_build", {}, status="failed")
    decision = decide_retry(record, attempt=3, policy=RetryPolicy("RETRY-0001", max_attempts=3), failure_message="temporary failure")
    assert decision.decision == "send_to_failed_jobs"


def test_decide_retry_unsupported_job_type() -> None:
    record = QueueRecord("JOB-0001", "unknown", {}, status="failed")
    decision = decide_retry(record, attempt=1, policy=RetryPolicy("RETRY-0001"), failure_message="Unsupported job type: unknown")
    assert decision.decision == "do_not_retry"


def test_create_failed_job() -> None:
    record = QueueRecord("JOB-0001", "unknown", {"x": 1}, status="failed")
    failed = create_failed_job(record, "Unsupported job type: unknown", attempt=1)
    data = failed.to_dict()
    assert data["failed_job"]["id"] == "FAILED-JOB-0001"
    assert data["failed_job"]["failure_class"] == "unsupported_job_type"
    assert data["payload"] == {"x": 1}
