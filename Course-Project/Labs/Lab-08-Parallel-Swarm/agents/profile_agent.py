
import json
import asyncio
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "Labs" / "Lab-02-Tool-Using-Agent" / "data"


def load_students():
    """Load student profiles from Lab 2."""
    file_path = DATA_DIR / "student_profiles.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def analyze_student_profile(student_id):
    """Analyse the academic and technical profile of a student."""
    students = load_students()

    if isinstance(students, dict):
        students = students.get("students", [])

    student = next(
        (
            item for item in students
            if item.get("student_id") == student_id
        ),
        None
    )

    if not student:
        return {
            "agent": "Profile Analyst",
            "status": "error",
            "message": f"Student {student_id} was not found."
        }

    cgpa = float(student.get("cgpa", 0))
    backlogs = int(student.get("active_backlogs", student.get("backlogs", 0)))
    skills = student.get("skills", [])

    return {
        "agent": "Profile Analyst",
        "status": "success",
        "student_id": student_id,
        "student_name": student.get("full_name", student.get("name", "Unknown")),
        "branch": student.get("branch", "Unknown"),
        "cgpa": cgpa,
        "backlogs": backlogs,
        "skills": skills,
        "academic_summary": (
            "Strong academic profile" if cgpa >= 8
            else "Moderate academic profile" if cgpa >= 7
            else "Academic profile needs improvement"
        ),
        "skill_count": len(skills)
    }


async def run_profile_agent(student_id):
    """Run profile analysis asynchronously."""
    return await asyncio.to_thread(
        analyze_student_profile,
        student_id
    )
