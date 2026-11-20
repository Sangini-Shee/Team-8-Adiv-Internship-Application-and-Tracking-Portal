
import json
from pathlib import Path

from resilience.logger import get_logger
from resilience.retry_handler import retry
from resilience.recovery import (
    recover_from_failure,
    validate_student_id
)


logger = get_logger("ResilientAgent")

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = (
    PROJECT_ROOT
    / "Labs"
    / "Lab-02-Tool-Using-Agent"
    / "data"
)


@retry(max_attempts=3, delay=1)
def load_student_data():
    """Load student records with automatic retry."""

    file_path = DATA_DIR / "student_profiles.json"

    logger.info("Loading student records from %s", file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Student dataset not found: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("students", []) if isinstance(data, dict) else data


def find_student(student_id):
    """Find a student in the dataset."""

    students = load_student_data()

    for student in students:
        if student.get("student_id") == student_id:
            return student

    raise LookupError(
        f"Student {student_id} was not found."
    )


def process_student(student_id):
    """Process student data with validation and recovery."""

    logger.info("Starting student processing.")

    try:
        student_id = validate_student_id(student_id)

        student = find_student(student_id)

        result = {
            "status": "success",
            "student": student,
            "message": "Student information retrieved successfully."
        }

        logger.info(
            "Successfully processed student %s",
            student_id
        )

        return result

    except (ValueError, LookupError, OSError, json.JSONDecodeError) as error:
        logger.warning("Student processing failed: %s", error)

        return recover_from_failure(
            error,
            fallback={
                "student_id": student_id,
                "recommendation": "Check the student ID or dataset."
            }
        )

    except Exception as error:
        logger.exception("Unexpected processing failure")

        return recover_from_failure(error)


def simulate_unstable_operation(failures_before_success=2):
    """Simulate a service that temporarily fails before succeeding."""

    if failures_before_success < 0:
        raise ValueError("Failure count cannot be negative.")

    attempts = {"count": 0}

    @retry(max_attempts=4, delay=0.2)
    def unstable_operation():
        attempts["count"] += 1

        logger.info(
            "Unstable operation attempt %s",
            attempts["count"]
        )

        if attempts["count"] <= failures_before_success:
            raise ConnectionError("Temporary service unavailable.")

        return {
            "status": "success",
            "attempts": attempts["count"],
            "message": "Service recovered successfully."
        }

    try:
        return unstable_operation()

    except ConnectionError as error:
        return recover_from_failure(
            error,
            fallback={"attempts": attempts["count"]}
        )
