
from typing import TypedDict, Any


class InternshipState(TypedDict, total=False):
    student_id: str
    student: dict
    opportunities: list
    recommendations: list
    messages: list
    status: str
    error: str
