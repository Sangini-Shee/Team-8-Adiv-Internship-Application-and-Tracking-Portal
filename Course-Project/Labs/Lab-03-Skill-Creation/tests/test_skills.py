
from app.skills import (
    opportunity_discovery,
    eligibility_verification,
    application_preparation
)

from app.schemas import (
    OpportunityDiscoveryInput,
    EligibilityVerificationInput,
    ApplicationPreparationInput
)

from app.skill_registry import list_skills, get_skill


def test_skill_registry():
    skills = list_skills()

    assert len(skills) == 3
    assert "opportunity_discovery" in skills
    assert "eligibility_verification" in skills
    assert "application_preparation" in skills


def test_get_existing_skill():
    skill = get_skill("opportunity_discovery")

    assert skill is not None
    assert skill["name"] == "Opportunity Discovery"


def test_opportunity_discovery():
    result = opportunity_discovery(
        OpportunityDiscoveryInput(
            student_id="STU001",
            preferred_domain="Artificial Intelligence"
        )
    )

    assert result.student_id == "STU001"
    assert result.total_found >= 1
    assert result.opportunities[0]["opportunity_id"] == "INT001"


def test_eligibility_verification():
    result = eligibility_verification(
        EligibilityVerificationInput(
            student_id="STU001",
            opportunity_id="INT001"
        )
    )

    assert result.status == "review_required"
    assert result.can_proceed_to_application is False


def test_application_preparation():
    result = application_preparation(
        ApplicationPreparationInput(
            student_id="STU001",
            opportunity_id="INT001",
            resume_available=True,
            cover_letter_available=False
        )
    )

    assert result.readiness_status == "review_required"
    assert result.student_id == "STU001"
    assert "Prepare updated resume" not in result.checklist


def test_invalid_student():
    try:
        opportunity_discovery(
            OpportunityDiscoveryInput(student_id="STU999")
        )
        assert False, "Expected ValueError for invalid student"
    except ValueError:
        assert True
