
import re


def analyze_requirements(project_description):
    """Extract functional and non-functional requirements."""

    if not isinstance(project_description, str) or not project_description.strip():
        raise ValueError("Project description cannot be empty.")

    description = project_description.strip()

    sentences = [
        item.strip()
        for item in re.split(r"[.\n;]+", description)
        if item.strip()
    ]

    functional_keywords = [
        "user", "login", "register", "manage", "create",
        "generate", "upload", "search", "track", "submit",
        "approve", "recommend", "display", "retrieve"
    ]

    non_functional_keywords = [
        "secure", "security", "fast", "performance",
        "reliable", "scalable", "available", "maintainable",
        "privacy", "responsive"
    ]

    functional = []
    non_functional = []

    for sentence in sentences:
        lower = sentence.lower()

        if any(word in lower for word in functional_keywords):
            functional.append(sentence)

        if any(word in lower for word in non_functional_keywords):
            non_functional.append(sentence)

    if not functional:
        functional = sentences.copy()

    return {
        "agent": "Requirement Analysis Agent",
        "status": "completed",
        "project_description": description,
        "functional_requirements": functional,
        "non_functional_requirements": non_functional,
        "total_requirements": len(functional) + len(non_functional)
    }
