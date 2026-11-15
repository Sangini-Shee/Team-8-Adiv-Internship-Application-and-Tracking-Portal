
from pydantic import BaseModel, Field
from typing import Literal


class OpportunityDiscoveryInput(BaseModel):
    student_id: str
    preferred_domain: str = "Any"
    preferred_work_mode: str = "Any"


class OpportunityDiscoveryOutput(BaseModel):
    student_id: str
    opportunities: list[dict]
    total_found: int


class EligibilityVerificationInput(BaseModel):
    student_id: str
    opportunity_id: str


class EligibilityVerificationOutput(BaseModel):
    student_id: str
    opportunity_id: str
    status: Literal[
        "eligible",
        "ineligible",
        "review_required"
    ]
    reasons: list[str]
    can_proceed_to_application: bool


class ApplicationPreparationInput(BaseModel):
    student_id: str
    opportunity_id: str
    resume_available: bool = False
    cover_letter_available: bool = False


class ApplicationPreparationOutput(BaseModel):
    student_id: str
    opportunity_id: str
    checklist: list[str]
    readiness_status: Literal[
        "ready",
        "incomplete",
        "review_required"
    ]
    message: str
