
# ============================================================
# LAB 2 - TOOL-USING AGENT
# File: app/tools.py
#
# Three tools:
# 1. read_student_profile()
# 2. read_opportunity()
# 3. check_eligibility()
# ============================================================

import json
from pathlib import Path

from app.schemas import (
    StudentProfile,
    InternshipOpportunity,
    EligibilityRules,
    EligibilityResult
)


# ------------------------------------------------------------
# DATA FILE LOCATIONS
# ------------------------------------------------------------

LAB_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = LAB_DIR / "data"

STUDENT_FILE = DATA_DIR / "student_profiles.json"
OPPORTUNITY_FILE = DATA_DIR / "opportunities.json"
RULES_FILE = DATA_DIR / "eligibility_rules.json"


# ------------------------------------------------------------
# COMMON JSON READER
# ------------------------------------------------------------

def load_json(file_path: Path) -> dict:
    """
    Loads a JSON file and returns its contents.

    Raises an error if the file is missing or invalid.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required data file not found: {file_path}"
        )

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {file_path.name}: {error}"
        ) from error


# ------------------------------------------------------------
# TOOL 1: READ STUDENT PROFILE
# ------------------------------------------------------------

def read_student_profile(student_id: str) -> StudentProfile:
    """
    Retrieves a student profile using the student ID.

    Example:
        read_student_profile("STU001")
    """

    if not student_id or not student_id.strip():
        raise ValueError("Student ID cannot be empty.")

    data = load_json(STUDENT_FILE)

    students = data.get("students", [])

    for student in students:

        if student.get("student_id") == student_id.strip():

            # Validate the retrieved record using Pydantic
            return StudentProfile.model_validate(student)

    raise ValueError(
        f"No student profile found for ID: {student_id}"
    )


# ------------------------------------------------------------
# TOOL 2: READ INTERNSHIP OPPORTUNITY
# ------------------------------------------------------------

def read_opportunity(
    opportunity_id: str
) -> InternshipOpportunity:
    """
    Retrieves an internship opportunity using its ID.

    Example:
        read_opportunity("INT001")
    """

    if not opportunity_id or not opportunity_id.strip():
        raise ValueError("Opportunity ID cannot be empty.")

    data = load_json(OPPORTUNITY_FILE)

    opportunities = data.get("opportunities", [])

    for opportunity in opportunities:

        if opportunity.get("opportunity_id") == opportunity_id.strip():

            # Validate the retrieved record using Pydantic
            return InternshipOpportunity.model_validate(
                opportunity
            )

    raise ValueError(
        f"No internship opportunity found for ID: {opportunity_id}"
    )


# ------------------------------------------------------------
# TOOL 3: CHECK ELIGIBILITY
# ------------------------------------------------------------

def check_eligibility(
    student_id: str,
    opportunity_id: str
) -> EligibilityResult:
    """
    Checks a student's eligibility against:

    1. Current configured institutional rules.
    2. Internship-specific requirements.
    3. Branch compatibility.
    4. Required skills.
    5. Data verification status.

    Demo records never receive final application approval.
    """

    # Retrieve actual records using the other tools
    student = read_student_profile(student_id)

    opportunity = read_opportunity(opportunity_id)

    rules_data = load_json(RULES_FILE)

    if "rules" not in rules_data:
        raise ValueError(
            "Eligibility rules are missing from the rules file."
        )

    rules = EligibilityRules.model_validate(
        rules_data["rules"]
    )

    # --------------------------------------------------------
    # DATA VALIDATION
    # --------------------------------------------------------

    if student.academic_year != rules.academic_year:
        return EligibilityResult(
            student_id=student.student_id,
            opportunity_id=opportunity.opportunity_id,
            status="review_required",
            checks={},
            reasons=[
                "Student academic year does not match "
                "the configured eligibility rules."
            ],
            rule_source=rules.authority,
            opportunity_approval_status=opportunity.approval_status,
            can_proceed_to_application=False
        )

    # --------------------------------------------------------
    # INSTITUTIONAL ELIGIBILITY CHECKS
    # --------------------------------------------------------

    institution_cgpa = (
        student.cgpa >= rules.min_cgpa
    )

    institution_backlogs = (
        student.active_backlogs <= rules.max_active_backlogs
    )

    institution_credits = (
        student.completed_credits >= rules.min_completed_credits
    )

    # --------------------------------------------------------
    # OPPORTUNITY-SPECIFIC CHECKS
    # --------------------------------------------------------

    branch_match = (
        student.branch.strip().casefold()
        in [
            branch.strip().casefold()
            for branch in opportunity.eligible_branches
        ]
    )

    opportunity_cgpa = (
        student.cgpa >= opportunity.min_cgpa
    )

    opportunity_backlogs = (
        student.active_backlogs
        <= opportunity.max_active_backlogs
    )

    opportunity_credits = (
        student.completed_credits
        >= opportunity.min_completed_credits
    )

    student_skills = {
        skill.strip().casefold()
        for skill in student.skills
    }

    required_skills = {
        skill.strip().casefold()
        for skill in opportunity.required_skills
    }

    missing_skills = sorted(
        required_skills - student_skills
    )

    skills_match = len(missing_skills) == 0

    # --------------------------------------------------------
    # COMBINE CHECK RESULTS
    # --------------------------------------------------------

    checks = {
        "institution_cgpa": institution_cgpa,
        "institution_backlogs": institution_backlogs,
        "institution_credits": institution_credits,
        "branch_match": branch_match,
        "opportunity_cgpa": opportunity_cgpa,
        "opportunity_backlogs": opportunity_backlogs,
        "opportunity_credits": opportunity_credits,
        "skills_match": skills_match
    }

    reasons = []

    if not institution_cgpa:
        reasons.append(
            f"CGPA is below the configured institutional "
            f"threshold of {rules.min_cgpa}."
        )

    if not institution_backlogs:
        reasons.append(
            f"Active backlogs exceed the configured "
            f"maximum of {rules.max_active_backlogs}."
        )

    if not institution_credits:
        reasons.append(
            f"Completed credits are below the configured "
            f"minimum of {rules.min_completed_credits}."
        )

    if not branch_match:
        reasons.append(
            "Student branch does not match the opportunity's "
            "eligible branches."
        )

    if not opportunity_cgpa:
        reasons.append(
            f"CGPA is below the opportunity requirement "
            f"of {opportunity.min_cgpa}."
        )

    if not opportunity_backlogs:
        reasons.append(
            "Active backlogs exceed the opportunity's "
            "maximum allowed backlogs."
        )

    if not opportunity_credits:
        reasons.append(
            "Completed credits are below the opportunity's "
            "minimum credit requirement."
        )

    if missing_skills:
        reasons.append(
            "Missing required skills: "
            + ", ".join(missing_skills)
        )

    all_checks_passed = all(checks.values())

    # --------------------------------------------------------
    # TRUST AND APPROVAL VALIDATION
    # --------------------------------------------------------

    demo_data = (
        student.data_status == "demo_only"
        or rules.approval_status != "faculty_approved"
        or opportunity.approval_status != "approved"
        or not opportunity.is_verified
    )

    if demo_data:

        status = "review_required"

        reasons.append(
            "This assessment uses demonstration or "
            "unapproved data. It is not an official "
            "eligibility decision."
        )

        if all_checks_passed:
            reasons.append(
                "All configured demonstration criteria passed."
            )
        else:
            reasons.append(
                "One or more configured demonstration criteria failed."
            )

    elif not all_checks_passed:

        status = "ineligible"

    else:

        status = "eligible"

        reasons.append(
            "All configured institutional and "
            "opportunity-specific checks passed."
        )

    can_proceed = (
        status == "eligible"
        and not demo_data
    )

    return EligibilityResult(
        student_id=student.student_id,
        opportunity_id=opportunity.opportunity_id,
        status=status,
        checks=checks,
        reasons=reasons,
        rule_source=rules.authority,
        opportunity_approval_status=opportunity.approval_status,
        can_proceed_to_application=can_proceed
    )


# ------------------------------------------------------------
# TOOL REGISTRY
# ------------------------------------------------------------

AVAILABLE_TOOLS = {
    "read_student_profile": read_student_profile,
    "read_opportunity": read_opportunity,
    "check_eligibility": check_eligibility
}
