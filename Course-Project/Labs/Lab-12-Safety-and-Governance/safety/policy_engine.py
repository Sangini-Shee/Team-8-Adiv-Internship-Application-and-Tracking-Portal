
SENSITIVE_ACTIONS = [
    "approve internship",
    "approve application",
    "reject application",
    "submit application",
    "upload offer letter",
    "change student record",
    "delete student record",
    "modify eligibility"
]


def evaluate_policy(action):
    """Evaluate an action against governance policies."""

    if not isinstance(action, str) or not action.strip():
        return {
            "allowed": False,
            "requires_human_approval": False,
            "status": "blocked",
            "reason": "Action cannot be empty."
        }

    normalized_action = action.strip().lower()

    for sensitive_action in SENSITIVE_ACTIONS:
        if sensitive_action in normalized_action:
            return {
                "allowed": True,
                "requires_human_approval": True,
                "status": "review_required",
                "reason": (
                    "This action requires human approval "
                    "before execution."
                ),
                "matched_policy": sensitive_action
            }

    return {
        "allowed": True,
        "requires_human_approval": False,
        "status": "approved",
        "reason": "Action complies with the configured policies.",
        "matched_policy": None
    }
