
import json
from pathlib import Path

from app.schemas import (
    OpportunityDiscoveryInput,
    OpportunityDiscoveryOutput,
    EligibilityVerificationInput,
    EligibilityVerificationOutput,
    ApplicationPreparationInput,
    ApplicationPreparationOutput
)


# Reuse Lab 2's demonstration data
DATA_DIR = (
    Path(__file__).resolve().parents[3]
    / "Labs"
    / "Lab-02-Tool-Using-Agent"
    / "data"
)


def load_data(filename):
    path = DATA_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def opportunity_discovery(
    request: OpportunityDiscoveryInput
) -> OpportunityDiscoveryOutput:
    """Discover opportunities matching student preferences."""

    students = load_data("student_profiles.json")["students"]
    opportunities = load_data("opportunities.json")["opportunities"]

    student = next(
        (s for s in students if s["student_id"] == request.student_id),
        None
    )

    if student is None:
        raise ValueError("Student ID not found.")

    student_skills = {
        skill.lower() for skill in student.get("skills", [])
    }

    matches = []

    for opportunity in opportunities:

        if request.preferred_domain.lower() not in ("any", opportunity["domain"].lower()):
            continue

        if request.preferred_work_mode.lower() not in ("any", opportunity["work_mode"].lower()):
            continue

        required_skills = {
            skill.lower() for skill in opportunity["required_skills"]
        }

        if required_skills.issubset(student_skills):
            matches.append(opportunity)

    return OpportunityDiscoveryOutput(
        student_id=request.student_id,
        opportunities=matches,
        total_found=len(matches)
    )


def eligibility_verification(
    request: EligibilityVerificationInput
) -> EligibilityVerificationOutput:
    """Verify eligibility using the existing Lab 2 rules."""

    students = load_data("student_profiles.json")["students"]
    opportunities = load_data("opportunities.json")["opportunities"]
    rules = load_data("eligibility_rules.json")["rules"]

    student = next(
        (s for s in students if s["student_id"] == request.student_id),
        None
    )

    opportunity = next(
        (o for o in opportunities if o["opportunity_id"] == request.opportunity_id),
        None
    )

    if student is None:
        raise ValueError("Student ID not found.")

    if opportunity is None:
        raise ValueError("Opportunity ID not found.")

    checks = {
        "academic_year": student["academic_year"] == rules["academic_year"],
        "institution_cgpa": student["cgpa"] >= rules["min_cgpa"],
        "institution_backlogs": student["active_backlogs"] <= rules["max_active_backlogs"],
        "institution_credits": student["completed_credits"] >= rules["min_completed_credits"],
        "branch": student["branch"] in opportunity["eligible_branches"],
        "opportunity_cgpa": student["cgpa"] >= opportunity["min_cgpa"],
        "opportunity_backlogs": student["active_backlogs"] <= opportunity["max_active_backlogs"],
        "opportunity_credits": student["completed_credits"] >= opportunity["min_completed_credits"],
        "skills": set(s.lower() for s in opportunity["required_skills"]).issubset(
            set(s.lower() for s in student["skills"])
        )
    }

    reasons = [
        name for name, passed in checks.items() if not passed
    ]

    verified = (
        student.get("data_status") == "verified"
        and opportunity.get("approval_status") == "approved"
        and opportunity.get("is_verified") is True
        and rules.get("approval_status") == "faculty_approved"
    )

    if not verified:
        status = "review_required"
    elif reasons:
        status = "ineligible"
    else:
        status = "eligible"

    return EligibilityVerificationOutput(
        student_id=request.student_id,
        opportunity_id=request.opportunity_id,
        status=status,
        reasons=reasons,
        can_proceed_to_application=(status == "eligible")
    )


def application_preparation(
    request: ApplicationPreparationInput
) -> ApplicationPreparationOutput:
    """Prepare an application checklist after eligibility verification."""

    eligibility = eligibility_verification(
        EligibilityVerificationInput(
            student_id=request.student_id,
            opportunity_id=request.opportunity_id
        )
    )

    checklist = [
        "Verify student profile information",
        "Review internship requirements",
        "Prepare updated resume",
        "Prepare application cover letter",
        "Obtain required institutional approvals"
    ]

    if request.resume_available:
        checklist.remove("Prepare updated resume")

    if request.cover_letter_available:
        checklist.remove("Prepare application cover letter")

    if eligibility.status == "ineligible":
        readiness = "incomplete"
        message = "The student does not meet the configured eligibility criteria."
    elif eligibility.status == "review_required":
        readiness = "review_required"
        message = "Official eligibility verification is required before proceeding."
    elif checklist:
        readiness = "incomplete"
        message = "Some application preparation steps are still pending."
    else:
        readiness = "ready"
        message = "The application preparation checklist is complete."

    return ApplicationPreparationOutput(
        student_id=request.student_id,
        opportunity_id=request.opportunity_id,
        checklist=checklist,
        readiness_status=readiness,
        message=message
    )
