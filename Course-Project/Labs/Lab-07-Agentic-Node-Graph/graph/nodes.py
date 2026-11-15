
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = (
    PROJECT_ROOT
    / "Labs"
    / "Lab-02-Tool-Using-Agent"
    / "data"
)


def load_json(filename):
    """Load JSON data from the Lab 2 dataset."""

    path = DATA_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_records(data, key):
    """Extract records from either a list or dictionary."""

    if isinstance(data, list):
        return data

    return data.get(key, [])


def retrieve_student(state):
    """Node 1: Retrieve student profile."""

    student_id = state.get("student_id", "").strip()

    if not student_id:
        return {
            "status": "failed",
            "error": "Student ID is required."
        }

    data = load_json("student_profiles.json")
    students = get_records(data, "students")

    student = next(
        (
            item for item in students
            if item.get("student_id") == student_id
        ),
        None
    )

    if student is None:
        return {
            "status": "failed",
            "error": f"Student {student_id} was not found."
        }

    return {
        "student": student,
        "status": "student_retrieved",
        "messages": ["Student profile retrieved."]
    }


def retrieve_opportunities(state):
    """Node 2: Retrieve internship opportunities."""

    if not state.get("student"):
        return {
            "status": "failed",
            "error": "Student profile is unavailable."
        }

    data = load_json("opportunities.json")
    opportunities = get_records(data, "opportunities")

    return {
        "opportunities": opportunities,
        "status": "opportunities_retrieved",
        "messages": ["Internship opportunities retrieved."]
    }


def recommend_opportunities(state):
    """Node 3: Recommend internships based on matching skills."""

    student = state.get("student", {})
    opportunities = state.get("opportunities", [])

    student_skills = {
        str(skill).lower()
        for skill in student.get("skills", [])
    }

    recommendations = []

    for opportunity in opportunities:

        required_skills = {
            str(skill).lower()
            for skill in opportunity.get(
                "required_skills",
                opportunity.get("skills", [])
            )
        }

        matched_skills = student_skills.intersection(
            required_skills
        )

        if matched_skills:
            recommendations.append({
                "internship": opportunity,
                "matched_skills": sorted(matched_skills),
                "match_count": len(matched_skills)
            })

    recommendations.sort(
        key=lambda item: item["match_count"],
        reverse=True
    )

    return {
        "recommendations": recommendations,
        "status": "recommendations_generated",
        "messages": ["Internship recommendations generated."]
    }


def finalize(state):
    """Node 4: Finalize the agent workflow."""

    if state.get("error"):
        return {
            "status": "failed",
            "messages": ["Agent workflow failed."]
        }

    return {
        "status": "completed",
        "messages": ["Agent workflow completed."]
    }
