
from typing import Literal
from pydantic import BaseModel, Field


# ------------------------------------------------
# STUDENT PROFILE
# ------------------------------------------------

class StudentProfile(BaseModel):
    student_id: str
    full_name: str
    branch: str
    cgpa: float = Field(ge=0, le=10)
    active_backlogs: int = Field(ge=0)
    completed_credits: int = Field(ge=0)
    skills: list[str] = Field(default_factory=list)
    academic_year: str
    semester: int = Field(ge=1, le=8)
    data_status: Literal["demo_only", "verified"] = "demo_only"


# ------------------------------------------------
# INTERNSHIP OPPORTUNITY
# ------------------------------------------------

class InternshipOpportunity(BaseModel):
    opportunity_id: str
    title: str
    company: str
    domain: str
    eligible_branches: list[str]
    required_skills: list[str]
    min_cgpa: float = Field(ge=0, le=10)
    max_active_backlogs: int = Field(ge=0)
    min_completed_credits: int = Field(ge=0)
    work_mode: str
    duration_months: int = Field(gt=0)
    posting_date: str
    source: str
    approval_status: Literal[
        "approved",
        "pending",
        "demo_only"
    ]
    is_verified: bool


# ------------------------------------------------
# ELIGIBILITY RULES
# ------------------------------------------------

class EligibilityRules(BaseModel):
    academic_year: str
    min_cgpa: float = Field(ge=0, le=10)
    max_active_backlogs: int = Field(ge=0)
    min_completed_credits: int = Field(ge=0)
    authority: str
    approval_status: Literal[
        "faculty_approved",
        "draft_demo"
    ]


# ------------------------------------------------
# ELIGIBILITY RESULT
# ------------------------------------------------

class EligibilityResult(BaseModel):
    student_id: str
    opportunity_id: str

    status: Literal[
        "eligible",
        "ineligible",
        "review_required"
    ]

    checks: dict[str, bool]
    reasons: list[str]

    rule_source: str
    opportunity_approval_status: str

    can_proceed_to_application: bool
