
import pytest

from resilience.retry_handler import retry
from resilience.recovery import (
    recover_from_failure,
    validate_student_id
)
from resilience.resilient_agent import (
    process_student,
    simulate_unstable_operation
)


def test_student_processing_success():
    result = process_student("STU001")

    assert result["status"] == "success"
    assert result["student"]["student_id"] == "STU001"


def test_invalid_student_recovery():
    result = process_student("INVALID")

    assert result["status"] == "recovered"
    assert "not found" in result["error"]


def test_empty_student_id_recovery():
    result = process_student("")

    assert result["status"] == "recovered"


def test_student_id_validation():
    assert validate_student_id(" STU001 ") == "STU001"

    with pytest.raises(ValueError):
        validate_student_id("")


def test_recovery_fallback():
    result = recover_from_failure(
        RuntimeError("Test error"),
        fallback={"action": "retry later"}
    )

    assert result["status"] == "recovered"
    assert result["fallback"]["action"] == "retry later"


def test_retry_success_after_failures():
    attempts = {"count": 0}

    @retry(max_attempts=3, delay=0)
    def temporary_failure():
        attempts["count"] += 1

        if attempts["count"] < 3:
            raise ConnectionError("Temporary failure")

        return "success"

    result = temporary_failure()

    assert result == "success"
    assert attempts["count"] == 3


def test_retry_exhaustion():
    attempts = {"count": 0}

    @retry(max_attempts=3, delay=0)
    def permanent_failure():
        attempts["count"] += 1
        raise ConnectionError("Service unavailable")

    with pytest.raises(ConnectionError):
        permanent_failure()

    assert attempts["count"] == 3


def test_retry_invalid_configuration():
    with pytest.raises(ValueError):
        retry(max_attempts=0)


def test_unstable_operation_recovers():
    result = simulate_unstable_operation(
        failures_before_success=2
    )

    assert result["status"] == "success"
    assert result["attempts"] == 3


def test_unstable_operation_exhaustion():
    result = simulate_unstable_operation(
        failures_before_success=5
    )

    assert result["status"] == "recovered"
