import pytest

from agents.academic_agent import AcademicAgent
from agents.skills_agent import SkillsAgent
from agents.career_agent import CareerAgent
from agents.application_agent import ApplicationAgent
from orchestrator.coordinator import DisciplineCoordinator


@pytest.fixture
def student():
    return {
        "student_id": "STU001",
        "name": "Sangini Shee",
        "cgpa": 8.4,
        "backlogs": 0,
        "credits_completed": 150,
        "skills": ["Python", "ML", "SQL", "Data Analysis"]
    }


@pytest.fixture
def internship():
    return {
        "internship_id": "INT001",
        "title": "AI/ML Intern",
        "min_cgpa": 7.0,
        "max_backlogs": 0,
        "min_credits": 140,
        "required_skills": ["Python", "ML"]
    }


def test_academic_agent_pass(student, internship):
    result = AcademicAgent().analyze(student, internship)

    assert result["eligible"] is True


def test_academic_agent_fail(student, internship):
    student["cgpa"] = 5.0

    result = AcademicAgent().analyze(student, internship)

    assert result["eligible"] is False


def test_academic_backlog_check(student, internship):
    student["backlogs"] = 2

    result = AcademicAgent().analyze(student, internship)

    assert result["checks"]["backlogs"] is False


def test_skills_agent_match(student, internship):
    result = SkillsAgent().analyze(student, internship)

    assert "python" in result["matched_skills"]
    assert result["match_percentage"] == 100


def test_skills_agent_missing(student, internship):
    internship["required_skills"] = [
        "Python", "ML", "TensorFlow"
    ]

    result = SkillsAgent().analyze(student, internship)

    assert "tensorflow" in result["missing_skills"]


def test_career_agent_recommendation(student, internship):
    academic = AcademicAgent().analyze(student, internship)
    skills = SkillsAgent().analyze(student, internship)

    result = CareerAgent().recommend(
        academic, skills, internship
    )

    assert result["recommendation"] == "Recommended"


def test_career_agent_not_eligible(student, internship):
    student["cgpa"] = 4.0

    academic = AcademicAgent().analyze(student, internship)
    skills = SkillsAgent().analyze(student, internship)

    result = CareerAgent().recommend(
        academic, skills, internship
    )

    assert result["recommendation"] == "Not eligible"


def test_application_agent(student, internship):
    career_result = {
        "recommendation": "Recommended"
    }

    result = ApplicationAgent().prepare(
        student, internship, career_result
    )

    summary = result["application_summary"]

    assert summary["student_name"] == "Sangini Shee"
    assert summary["application_status"] == (
        "Draft - Awaiting Student Submission"
    )


def test_coordinator(student, internship):
    result = DisciplineCoordinator().analyze_application(
        student, internship
    )

    assert result["student"] == "Sangini Shee"
    assert "academic_analysis" in result
    assert "skills_analysis" in result
    assert "career_recommendation" in result
    assert "application_preparation" in result


def test_coordinator_rejects_ineligible_student(student, internship):
    student["cgpa"] = 4.0

    result = DisciplineCoordinator().analyze_application(
        student, internship
    )

    assert result["career_recommendation"]["recommendation"] == (
        "Not eligible"
    )