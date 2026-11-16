
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "Labs" / "Lab-02-Tool-Using-Agent" / "data"


def load_json(filename):
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def extract_records(data, key):
    if isinstance(data, dict):
        return data.get(key, [])
    return data


def retrieve_evidence(student_id):
    """
    Retrieve student and internship records as evidence.
    Each record receives a unique evidence ID.
    """

    student_data = load_json("student_profiles.json")
    opportunity_data = load_json("opportunities.json")

    students = extract_records(student_data, "students")
    opportunities = extract_records(
        opportunity_data, "opportunities"
    )

    student = next(
        (
            item for item in students
            if item.get("student_id") == student_id
        ),
        None
    )

    if not student:
        return {
            "status": "error",
            "message": f"Student {student_id} was not found.",
            "evidence": []
        }

    evidence = [
        {
            "source_id": f"SRC-STUDENT-{student_id}",
            "source_type": "student_profile",
            "record_id": student_id,
            "content": student
        }
    ]

    for opportunity in opportunities:
        opportunity_id = (
            opportunity.get("internship_id")
            or opportunity.get("opportunity_id")
            or opportunity.get("id")
        )

        if not opportunity_id:
            opportunity_id = opportunity.get("title", "UNKNOWN")

        evidence.append({
            "source_id": f"SRC-INTERNSHIP-{opportunity_id}",
            "source_type": "internship_listing",
            "record_id": opportunity_id,
            "content": opportunity
        })

    return {
        "status": "success",
        "student_id": student_id,
        "evidence_count": len(evidence),
        "evidence": evidence
    }
