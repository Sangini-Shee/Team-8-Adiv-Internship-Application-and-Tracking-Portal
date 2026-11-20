
import json

from governance.orchestrator import run_governance
from safety.audit_logger import read_audit_logs


def main():
    print("=" * 65)
    print("          INTERNSHIP SAFETY AND GOVERNANCE SYSTEM")
    print("=" * 65)

    print("\n1. Execute an action")
    print("2. View audit logs")
    print("3. Exit")

    choice = input("\nSelect an option: ").strip()

    if choice == "1":

        action = input("\nEnter the action: ").strip()

        proposed_output = input(
            "Enter the proposed output: "
        ).strip()

        human_decision = None

        sensitive_actions = [
            "approve internship",
            "approve application",
            "reject application",
            "submit application",
            "upload offer letter",
            "change student record",
            "delete student record",
            "modify eligibility"
        ]

        if any(
            item in action.lower()
            for item in sensitive_actions
        ):
            decision = input(
                "\nHuman approval required. Approve? (yes/no): "
            ).strip().lower()

            if decision not in ["yes", "no"]:
                print("Invalid approval response.")
                return

            human_decision = decision == "yes"

        result = run_governance(
            action,
            proposed_output,
            human_decision
        )

        print("\n" + "=" * 65)
        print("                 GOVERNANCE RESULT")
        print("=" * 65)

        print(json.dumps(result, indent=4))

    elif choice == "2":

        logs = read_audit_logs()

        print("\n" + "=" * 65)
        print("                    AUDIT LOGS")
        print("=" * 65)

        if not logs:
            print("\nNo audit events recorded yet.")
        else:
            print(json.dumps(logs, indent=4))

    elif choice == "3":
        print("\nExiting application.")

    else:
        print("\nInvalid option.")


if __name__ == "__main__":
    main()
