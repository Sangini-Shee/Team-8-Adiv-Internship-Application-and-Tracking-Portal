
import json
from pathlib import Path

from agents.requirement_agent import analyze_requirements
from agents.design_agent import generate_design
from agents.code_agent import (
    generate_code_skeleton,
    save_generated_code
)
from agents.testing_agent import generate_test_plan
from agents.documentation_agent import generate_documentation


def run_sdlc_factory(project_name, project_description):
    """Execute the complete SDLC workflow."""

    if not project_name or not project_name.strip():
        raise ValueError("Project name cannot be empty.")

    print("\n[1/5] Running Requirement Analysis Agent...")
    requirements = analyze_requirements(project_description)

    print("[2/5] Running Design Agent...")
    design = generate_design(requirements)

    print("[3/5] Running Code Generation Agent...")
    code = generate_code_skeleton(project_name, design)

    print("[4/5] Running Testing Agent...")
    testing = generate_test_plan(requirements, code)

    print("[5/5] Running Documentation Agent...")
    documentation = generate_documentation(
        project_name,
        requirements,
        design,
        code,
        testing
    )

    output_directory = (
        Path(__file__).resolve().parents[1] / "outputs"
    )

    output_directory.mkdir(exist_ok=True)

    generated_project_path = save_generated_code(
        code,
        output_directory / "generated_projects"
    )

    documentation_file = (
        output_directory / "project_documentation.md"
    )

    documentation_file.write_text(
        documentation["documentation"],
        encoding="utf-8"
    )

    result = {
        "status": "completed",
        "project_name": project_name,
        "agents_executed": 5,
        "requirement_analysis": requirements,
        "system_design": design,
        "code_generation": code,
        "testing_plan": testing,
        "documentation": documentation,
        "generated_project_path": generated_project_path,
        "documentation_path": str(documentation_file)
    }

    result_file = output_directory / "sdlc_factory_results.json"

    with open(result_file, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4)

    return result
