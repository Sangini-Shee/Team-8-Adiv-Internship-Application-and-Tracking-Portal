
from resilience.logger import get_logger


logger = get_logger("Recovery")


def recover_from_failure(error, fallback=None):
    """Handle an error and return a safe fallback response."""

    logger.error("Recovery initiated: %s", error)

    return {
        "status": "recovered",
        "error": str(error),
        "fallback": fallback,
        "message": "Operation failed, but the system recovered safely."
    }


def validate_student_id(student_id):
    """Validate student ID before processing."""

    if not isinstance(student_id, str) or not student_id.strip():
        raise ValueError("Student ID cannot be empty.")

    return student_id.strip()
