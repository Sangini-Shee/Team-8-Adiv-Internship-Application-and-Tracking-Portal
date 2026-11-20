"""MCP server exposing read-only internship portal tools.

Run from this directory:
    python mcp_server.py
The server uses stdio transport, suitable for MCP clients.
"""
from mcp.server.fastmcp import FastMCP
from db import init_db, seed_data, get_conn
from agents import assess_eligibility

mcp = FastMCP("Internship Portal MCP Server")


@mcp.tool()
def list_internships() -> list[dict]:
    """List active internship opportunities."""
    init_db()
    seed_data()
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, title, company, department, required_skills, "
            "min_cgpa, max_backlogs, min_credits, duration, mode "
            "FROM internships WHERE active=1"
        ).fetchall()
    return [dict(row) for row in rows]


@mcp.tool()
def get_student_profile(student_id: str) -> dict:
    """Retrieve a student profile by student ID."""
    init_db()
    seed_data()
    with get_conn() as conn:
        row = conn.execute(
            "SELECT student_id, full_name, department, cgpa, backlogs, "
            "credits, skills FROM students WHERE student_id=?",
            (student_id,)
        ).fetchone()
    return dict(row) if row else {"error": "Student not found."}


@mcp.tool()
def verify_eligibility(student_id: str, internship_id: int) -> dict:
    """Verify academic and skill eligibility for a student and internship."""
    init_db()
    seed_data()
    with get_conn() as conn:
        student = conn.execute(
            "SELECT * FROM students WHERE student_id=?", (student_id,)
        ).fetchone()
        internship = conn.execute(
            "SELECT * FROM internships WHERE id=?", (internship_id,)
        ).fetchone()
    if not student or not internship:
        return {"error": "Student or internship not found."}
    return assess_eligibility(dict(student), dict(internship))


if __name__ == "__main__":
    init_db()
    seed_data()
    mcp.run()
