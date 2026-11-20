
from safety.input_guard import validate_input
from safety.output_guard import validate_output
from safety.policy_engine import evaluate_policy
from safety.human_approval import request_human_approval
from safety.audit_logger import record_audit_event


def run_governance(action, proposed_output, human_decision=None):
    """Execute the complete safety and governance workflow."""

    result = {
        "status": "processing",
        "action": action,
        "input_validation": None,
        "policy_evaluation": None,
        "human_approval": None,
        "output_validation": None
    }

    # Step 1: Validate the input.
    input_result = validate_input(action)
    result["input_validation"] = input_result

    record_audit_event("INPUT_VALIDATION", input_result)

    if not input_result["safe"]:
        result["status"] = "blocked"
        record_audit_event("ACTION_BLOCKED", result)
        return result

    # Step 2: Evaluate organizational policies.
    policy_result = evaluate_policy(action)
    result["policy_evaluation"] = policy_result

    record_audit_event("POLICY_EVALUATION", policy_result)

    if not policy_result["allowed"]:
        result["status"] = "blocked"
        record_audit_event("ACTION_BLOCKED", result)
        return result

    # Step 3: Request human approval if necessary.
    if policy_result["requires_human_approval"]:

        approval_result = request_human_approval(
            action,
            human_decision
        )

        result["human_approval"] = approval_result

        record_audit_event("HUMAN_APPROVAL", approval_result)

        if approval_result["status"] == "pending":
            result["status"] = "pending_approval"
            return result

        if not approval_result["approved"]:
            result["status"] = "rejected"
            record_audit_event("ACTION_REJECTED", result)
            return result

    # Step 4: Validate the proposed output.
    output_result = validate_output(proposed_output)
    result["output_validation"] = output_result

    record_audit_event("OUTPUT_VALIDATION", output_result)

    if not output_result["safe"]:
        result["status"] = "blocked"
        record_audit_event("OUTPUT_BLOCKED", result)
        return result

    # Step 5: Mark the operation as completed.
    result["status"] = "approved"
    result["final_output"] = proposed_output

    record_audit_event("GOVERNANCE_COMPLETED", {
        "action": action,
        "status": "approved"
    })

    return result
