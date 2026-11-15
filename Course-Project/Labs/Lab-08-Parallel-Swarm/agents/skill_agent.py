
import json
import asyncio
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "Labs" / "Lab-02-Tool-Using-Agent" / "data"


def load_json(filename):
    file_path = DATA_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def match_student_skills(student_id):
    """Identify how a student's skills match internship requirements."""

    students_data = load_json("student_profiles.json")
    opportunities_data = load_json("opportunities.json")

    students = (
        students_data.get("students", [])
        if isinstance(students_data, dict)
        else students_data
    )

    opportunities = (
        opportunities_data.get("opportunities", [])
        if isinstance(opportunities_data, dict)
        else opportunities_data
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
            "agent": "Skill Matching Agent",
            "status": "error",
            "message": f"Student {student_id} was not found."
        }

    student_skills = {
        skill.strip().lower()
        for skill in student.get("skills", [])
    }

    matches = []

    for opportunity in opportunities:
        required_skills = opportunity.get(
            "required_skills",
            opportunity.get("skills", [])
        )

        required = {
            skill.strip().lower()
            for skill in required_skills
        }

        matched = sorted(student_skills.intersection(required))
        missing = sorted(required - student_skills)

        match_percentage = (
            round(len(matched) / len(required) * 100, 2)
            if required else 0
        )

        matches.append({
            "internship_id": opportunity.get(
    "internship_id",
    opportunity.get("opportunity_id", opportunity.get("id"))
),
            "title": opportunity.get("title", "Unknown"),
            "matched_skills": matched,
            "missing_skills": missing,
            "match_percentage": match_percentage
        })

    matches.sort(
        key=lambda item: item["match_percentage"],
        reverse=True
    )

    return {
        "agent": "Skill Matching Agent",
        "status": "success",
        "student_id": student_id,
        "student_skills": sorted(student_skills),
        "opportunity_matches": matches
    }


async def run_skill_agent(student_id):
    """Run skill matching asynchronously."""
    return await asyncio.to_thread(
        match_student_skills,
        student_id
    )
