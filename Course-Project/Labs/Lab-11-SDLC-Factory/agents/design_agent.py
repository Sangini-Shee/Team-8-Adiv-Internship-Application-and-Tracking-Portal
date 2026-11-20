
def generate_design(requirement_result):
    """Generate a high-level software system design."""

    if requirement_result.get("status") != "completed":
        raise ValueError("Valid requirement analysis is required.")

    functional = requirement_result.get(
        "functional_requirements", []
    )

    non_functional = requirement_result.get(
        "non_functional_requirements", []
    )

    components = [
        {
            "name": "User Interface",
            "responsibility": "Accept user input and display results."
        },
        {
            "name": "Application Layer",
            "responsibility": "Coordinate application workflows."
        },
        {
            "name": "Business Logic Layer",
            "responsibility": "Execute core application operations."
        },
        {
            "name": "Data Layer",
            "responsibility": "Store and retrieve application data."
        }
    ]

    return {
        "agent": "Design Agent",
        "status": "completed",
        "architecture": "Layered Architecture",
        "components": components,
        "functional_requirements_count": len(functional),
        "non_functional_requirements_count": len(non_functional),
        "design_principles": [
            "Modularity",
            "Separation of Concerns",
            "Maintainability",
            "Reusability"
        ]
    }
