"""Optional LangChain agent integration for the internship portal.

The deterministic local eligibility engine remains the source of truth.
The LLM agent is used only for explanatory assistance and cannot approve
or reject applications.
"""
import os

from langchain.tools import tool
from langchain.agents import create_agent

from db import get_conn
from agents import assess_eligibility


@tool
def lookup_internships() -> list[dict]:
    """List active internship opportunities and their eligibility criteria."""
    with get_conn() as conn:
        records = conn.execute(
            "SELECT id, title, company, required_skills, min_cgpa, "
            "max_backlogs, min_credits FROM internships WHERE active=1"
        ).fetchall()
    return [dict(row) for row in records]


@tool
def check_student_eligibility(student_id: str, internship_id: int) -> dict:
    """Check a student's academic and skill eligibility for an internship."""
    with get_conn() as conn:
        student = conn.execute(
            "SELECT * FROM students WHERE student_id=?", (student_id,)
        ).fetchone()
        internship = conn.execute(
            "SELECT * FROM internships WHERE id=?", (internship_id,)
        ).fetchone()
    if not student or not internship:
        return {"error": "Student or internship record not found."}
    return assess_eligibility(dict(student), dict(internship))


def build_langchain_agent():
    """Create a LangChain tool-calling agent when GOOGLE_API_KEY is configured."""
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError(
            "GOOGLE_API_KEY is not configured. Local portal features still work."
        )
    model = os.getenv("LANGCHAIN_MODEL", "google_genai:gemini-2.5-flash")
    return create_agent(
        model=model,
        tools=[lookup_internships, check_student_eligibility],
        system_prompt=(
            "You are an internship portal assistant. Use the provided tools "
            "for factual internship and eligibility data. Explain results "
            "clearly. Never claim an application is approved. Only the HOD and "
            "Internship Coordinator can make approval decisions in the portal."
        ),
    )


def ask_langchain(question: str) -> str:
    agent = build_langchain_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    messages = result.get("messages", [])
    return str(messages[-1].content) if messages else "No response returned."
