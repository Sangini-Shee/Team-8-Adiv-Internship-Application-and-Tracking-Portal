
from app.skill_registry import list_skills
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


def main():
    print("=" * 55)
    print("         INTERNSHIP REUSABLE SKILL CENTER")
    print("=" * 55)

    skills = list_skills()

    for index, skill in enumerate(skills.values(), start=1):
        print(f"{index}. {skill['name']} - {skill['description']}")

    print("\nDemonstration: Opportunity Discovery")

    result = opportunity_discovery(
        OpportunityDiscoveryInput(
            student_id="STU001",
            preferred_domain="Artificial Intelligence"
        )
    )

    print(result.model_dump_json(indent=2))

    print("\nDemonstration: Eligibility Verification")

    eligibility = eligibility_verification(
        EligibilityVerificationInput(
            student_id="STU001",
            opportunity_id="INT001"
        )
    )

    print(eligibility.model_dump_json(indent=2))

    print("\nDemonstration: Application Preparation")

    application = application_preparation(
        ApplicationPreparationInput(
            student_id="STU001",
            opportunity_id="INT001",
            resume_available=True
        )
    )

    print(application.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
