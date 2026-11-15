
import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Internship Portal MCP Server")

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = (
    PROJECT_ROOT
    / "Labs"
    / "Lab-02-Tool-Using-Agent"
    / "data"
)


def load_json(filename):
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


@mcp.tool()
def get_student_profile(student_id: str) -> dict:
    """Retrieve a student profile using the student ID."""
    data = load_json("student_profiles.json")
    students = data if isinstance(data, list) else data.get("students", [])

    for student in students:
        if student.get("student_id") == student_id:
            return student

    return {"error": f"No student found with ID {student_id}"}


@mcp.tool()
def list_internships() -> list:
    """List all internship opportunities available in the portal."""
    data = load_json("opportunities.json")
    return data if isinstance(data, list) else data.get("opportunities", [])


@mcp.tool()
def get_internship_details(internship_id: str) -> dict:
    """Retrieve detailed information about a specific internship."""
    internships = list_internships()

    for internship in internships:
        if internship.get("internship_id") == internship_id:
            return internship

    return {"error": f"No internship found with ID {internship_id}"}


if __name__ == "__main__":
    mcp.run()
