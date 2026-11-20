
def request_human_approval(action, decision=None):
    """Request and record a human approval decision."""

    if decision is None:
        return {
            "approved": False,
            "status": "pending",
            "action": action,
            "message": "Human approval is pending."
        }

    if not isinstance(decision, bool):
        return {
            "approved": False,
            "status": "invalid",
            "action": action,
            "message": "Approval decision must be True or False."
        }

    if decision:
        return {
            "approved": True,
            "status": "approved",
            "action": action,
            "message": "Action approved by human reviewer."
        }

    return {
        "approved": False,
        "status": "rejected",
        "action": action,
        "message": "Action rejected by human reviewer."
    }
