
# ============================================================
# LAB 1 - AGENT VS CHATBOT
# File: app/agent.py
# Purpose: Coordinator agent and clarify-plan-revise loop
# ============================================================

import os
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from google import genai

from app.prompts import (
    CLARIFICATION_PROMPT,
    PLANNING_PROMPT,
    REVISION_PROMPT
)


# ------------------------------------------------------------
# PROJECT CONFIGURATION
# ------------------------------------------------------------

# agent.py is located at:
# Repository/Course-Project/Labs/Lab-01/app/agent.py
PROJECT_ROOT = Path(__file__).resolve().parents[4]

load_dotenv(PROJECT_ROOT / ".env")


# ------------------------------------------------------------
# GEMINI CLIENT
# ------------------------------------------------------------

def get_gemini_response(prompt: str) -> str:
    """
    Sends a prompt to Gemini and returns its response.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "Gemini API key not found. "
            "Check the .env file in the repository root."
        )

    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text.strip()


# ------------------------------------------------------------
# STAGE 1: CLARIFICATION
# ------------------------------------------------------------

def clarify_request(student_request: str) -> str:
    """
    Analyzes the initial request and generates
    clarification questions.
    """

    if not student_request.strip():
        raise ValueError(
            "Student request cannot be empty."
        )

    prompt = CLARIFICATION_PROMPT.format(
        student_request=student_request
    )

    return get_gemini_response(prompt)


# ------------------------------------------------------------
# STAGE 2: PLAN GENERATION
# ------------------------------------------------------------

def create_plan(
    student_request: str,
    clarified_requirements: str
) -> str:
    """
    Generates an editable internship application outline.
    """

    if not student_request.strip():
        raise ValueError(
            "Student request cannot be empty."
        )

    if not clarified_requirements.strip():
        raise ValueError(
            "Clarification details cannot be empty."
        )

    prompt = PLANNING_PROMPT.format(
        student_request=student_request,
        clarified_requirements=clarified_requirements
    )

    return get_gemini_response(prompt)


# ------------------------------------------------------------
# STAGE 3: PLAN REVISION
# ------------------------------------------------------------

def revise_plan(
    existing_plan: str,
    feedback: str
) -> str:
    """
    Revises the existing outline based on student feedback.
    """

    if not existing_plan.strip():
        raise ValueError(
            "Existing plan cannot be empty."
        )

    if not feedback.strip():
        raise ValueError(
            "Revision feedback cannot be empty."
        )

    prompt = REVISION_PROMPT.format(
        existing_plan=existing_plan,
        feedback=feedback
    )

    return get_gemini_response(prompt)


# ------------------------------------------------------------
# SAVE FINAL OUTLINE
# ------------------------------------------------------------

def save_plan(plan: str) -> str:
    """
    Saves the editable outline as a Markdown file.
    """

    if not plan.strip():
        raise ValueError(
            "Cannot save an empty outline."
        )

    output_directory = (
        Path(__file__).resolve().parents[1] / "outputs"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = (
        output_directory /
        f"internship_outline_{timestamp}.md"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(plan)

    return str(output_file)
