
def generate_documentation(
    project_name,
    requirement_result,
    design_result,
    code_result,
    testing_result
):
    """Generate project documentation from SDLC outputs."""

    functional = requirement_result.get(
        "functional_requirements", []
    )

    non_functional = requirement_result.get(
        "non_functional_requirements", []
    )

    components = design_result.get("components", [])
    test_cases = testing_result.get("test_cases", [])

    lines = [
        f"# {project_name}",
        "",
        "## Overview",
        "This project was processed using the SDLC Factory.",
        "",
        "## Functional Requirements"
    ]

    lines.extend(
        f"- {item}" for item in functional
    )

    lines.extend([
        "",
        "## Non-Functional Requirements"
    ])

    lines.extend(
        f"- {item}" for item in non_functional
    )

    lines.extend([
        "",
        "## System Architecture",
        f"Architecture: {design_result['architecture']}",
        ""
    ])

    for component in components:
        lines.append(
            f"- **{component['name']}**: "
            f"{component['responsibility']}"
        )

    lines.extend([
        "",
        "## Generated Source Files"
    ])

    lines.extend(
        f"- {filename}"
        for filename in code_result["generated_files"]
    )

    lines.extend([
        "",
        "## Testing Plan",
        f"Total test cases: {len(test_cases)}",
        ""
    ])

    for test in test_cases:
        lines.append(
            f"- **{test['test_id']} – {test['test_name']}**: "
            f"{test['objective']}"
        )

    lines.extend([
        "",
        "## Conclusion",
        "The SDLC Factory generated a structured requirement analysis, "
        "system design, source-code skeleton, test plan and documentation."
    ])

    return {
        "agent": "Documentation Agent",
        "status": "completed",
        "documentation": "\n".join(lines)
    }
