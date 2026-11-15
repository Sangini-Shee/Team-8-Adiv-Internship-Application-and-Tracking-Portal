
# ============================================================
# LAB 1 - AGENT VS CHATBOT
# File: tests/test_agent.py
# Purpose: Automated acceptance and validation tests
# ============================================================

import pytest

from app.agent import (
    clarify_request,
    create_plan,
    revise_plan,
    save_plan
)


# ------------------------------------------------------------
# TEST 1: CLARIFICATION
# ------------------------------------------------------------

def test_clarification_agent(monkeypatch):

    def mock_response(prompt):
        assert "I want an internship." in prompt
        return (
            "1. Which internship domain interests you?\n"
            "2. What technical skills do you have?"
        )

    monkeypatch.setattr(
        "app.agent.get_gemini_response",
        mock_response
    )

    result = clarify_request(
        "I want an internship."
    )

    assert "internship domain" in result.lower()
    assert "technical skills" in result.lower()


# ------------------------------------------------------------
# TEST 2: PLAN GENERATION
# ------------------------------------------------------------

def test_planning_agent(monkeypatch):

    def mock_response(prompt):
        assert "I want an AI internship." in prompt
        assert "I know Python." in prompt

        return (
            "# Internship Application Outline\n"
            "Domain: Artificial Intelligence\n"
            "Skills: Python\n"
            "Status: Not started"
        )

    monkeypatch.setattr(
        "app.agent.get_gemini_response",
        mock_response
    )

    result = create_plan(
        "I want an AI internship.",
        "I know Python."
    )

    assert "Internship Application Outline" in result
    assert "Artificial Intelligence" in result


# ------------------------------------------------------------
# TEST 3: PLAN REVISION
# ------------------------------------------------------------

def test_revision_agent(monkeypatch):

    def mock_response(prompt):
        assert "Existing internship outline" in prompt
        assert "Add a two-week schedule" in prompt

        return (
            "# Revised Internship Application Outline\n"
            "Includes a two-week preparation schedule."
        )

    monkeypatch.setattr(
        "app.agent.get_gemini_response",
        mock_response
    )

    result = revise_plan(
        "Existing internship outline",
        "Add a two-week schedule"
    )

    assert "Revised Internship Application Outline" in result
    assert "two-week" in result


# ------------------------------------------------------------
# TEST 4: EMPTY STUDENT REQUEST
# ------------------------------------------------------------

def test_empty_student_request():

    with pytest.raises(ValueError):
        clarify_request("")


# ------------------------------------------------------------
# TEST 5: EMPTY CLARIFICATION ANSWERS
# ------------------------------------------------------------

def test_empty_clarification_answers():

    with pytest.raises(ValueError):
        create_plan(
            "I want an internship.",
            ""
        )


# ------------------------------------------------------------
# TEST 6: EMPTY REVISION FEEDBACK
# ------------------------------------------------------------

def test_empty_revision_feedback():

    with pytest.raises(ValueError):
        revise_plan(
            "Existing outline",
            ""
        )


# ------------------------------------------------------------
# TEST 7: SAVE OUTLINE
# ------------------------------------------------------------

def test_save_plan(tmp_path, monkeypatch):

    import app.agent as agent

    fake_agent_path = (
        tmp_path / "Lab-01" / "app" / "agent.py"
    )

    fake_agent_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    monkeypatch.setattr(
        agent,
        "__file__",
        str(fake_agent_path)
    )

    plan = "# Internship Application Outline\n\nTest content."

    file_path = save_plan(plan)

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        saved_content = file.read()

    assert "Internship Application Outline" in saved_content
    assert "Test content." in saved_content


# ------------------------------------------------------------
# TEST 8: EMPTY OUTLINE SAVE
# ------------------------------------------------------------

def test_empty_plan_save():

    with pytest.raises(ValueError):
        save_plan("")
