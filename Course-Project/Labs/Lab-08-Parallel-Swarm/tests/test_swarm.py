
import asyncio
import pytest

from agents.profile_agent import analyze_student_profile
from agents.skill_agent import match_student_skills
from agents.opportunity_agent import analyze_opportunities
from swarm.orchestrator import run_parallel_swarm


def test_profile_agent_success():
    result = analyze_student_profile("STU001")

    assert result["status"] == "success"
    assert result["student_name"] == "Sangini Shee"
    assert result["cgpa"] == 8.4


def test_profile_agent_invalid_student():
    result = analyze_student_profile("INVALID")

    assert result["status"] == "error"


def test_skill_agent_success():
    result = match_student_skills("STU001")

    assert result["status"] == "success"
    assert len(result["opportunity_matches"]) > 0


def test_skill_matching_percentage():
    result = match_student_skills("STU001")

    first_match = result["opportunity_matches"][0]

    assert first_match["match_percentage"] == 100.0


def test_opportunity_agent():
    result = analyze_opportunities()

    assert result["status"] == "success"
    assert result["total_opportunities"] >= 1


def test_parallel_swarm_execution():
    result = asyncio.run(run_parallel_swarm("STU001"))

    assert result["status"] == "completed"
    assert result["agents_executed"] == 3
    assert result["execution_mode"] == "parallel"


def test_parallel_swarm_invalid_student():
    result = asyncio.run(run_parallel_swarm("INVALID"))

    assert result["status"] == "partial"
    assert "profile_analysis" in result["agent_results"]


def test_empty_student_id():
    result = asyncio.run(run_parallel_swarm(""))

    assert result["status"] == "partial"


