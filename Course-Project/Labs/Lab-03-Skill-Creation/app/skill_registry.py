
SKILL_REGISTRY = {
    "opportunity_discovery": {
        "name": "Opportunity Discovery",
        "description": "Find internship opportunities matching a student's domain, skills and preferences.",
        "category": "Discovery"
    },
    "eligibility_verification": {
        "name": "Eligibility Verification",
        "description": "Verify whether a student meets the academic and opportunity requirements.",
        "category": "Verification"
    },
    "application_preparation": {
        "name": "Application Preparation",
        "description": "Prepare an application checklist and assess application readiness.",
        "category": "Application"
    }
}


def list_skills():
    """Return all registered skills."""
    return SKILL_REGISTRY


def get_skill(skill_name: str):
    """Retrieve a skill by its registered name."""
    return SKILL_REGISTRY.get(skill_name)
