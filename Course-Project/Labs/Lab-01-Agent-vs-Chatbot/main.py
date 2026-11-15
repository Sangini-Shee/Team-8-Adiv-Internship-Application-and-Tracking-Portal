
# ============================================================
# LAB 1 - AGENT VS CHATBOT
# File: main.py
# Purpose: Interactive internship application planner
# ============================================================

from app.agent import (
    clarify_request,
    create_plan,
    revise_plan,
    save_plan
)


def display_header():
    print("\n" + "=" * 70)
    print("       INTERNSHIP APPLICATION AND TRACKING PORTAL")
    print("                    LAB 1")
    print("                AGENT VS CHATBOT")
    print("=" * 70)

    print("\nWelcome to the Internship Application Planning Agent.")

    print(
        "\nThis agent follows an iterative workflow:"
        "\nClarify -> Plan -> Revise"
    )


def get_student_request():
    while True:
        request = input(
            "\nDescribe the internship you want to pursue:\n> "
        ).strip()

        if request:
            return request

        print("Please enter a valid request.")


def clarification_stage(student_request):
    print("\n" + "-" * 70)
    print("STAGE 1: CLARIFICATION")
    print("-" * 70)

    print("\n[COORDINATOR] Analyzing your request...")

    questions = clarify_request(student_request)

    print("\n[COORDINATOR] Additional information required:\n")
    print(questions)

    print(
        "\nAnswer the questions above. "
        "You can provide your answers in one response."
    )

    while True:
        answers = input("\nYour answers:\n> ").strip()

        if answers:
            return answers

        print("Please provide your clarification answers.")


def planning_stage(student_request, answers):
    print("\n" + "-" * 70)
    print("STAGE 2: PLAN GENERATION")
    print("-" * 70)

    print("\n[COORDINATOR] Preparing your application outline...")

    plan = create_plan(
        student_request,
        answers
    )

    print("\n" + "=" * 70)
    print("PROPOSED INTERNSHIP APPLICATION OUTLINE")
    print("=" * 70)

    print(plan)

    return plan


def revision_stage(plan):
    print("\n" + "-" * 70)
    print("STAGE 3: REVISION")
    print("-" * 70)

    while True:
        choice = input(
            "\nWould you like to revise the outline? (yes/no): "
        ).strip().lower()

        if choice in ("no", "n"):
            return plan

        if choice not in ("yes", "y"):
            print("Please enter yes or no.")
            continue

        feedback = input(
            "\nDescribe the changes you want:\n> "
        ).strip()

        if not feedback:
            print("Revision feedback cannot be empty.")
            continue

        print("\n[COORDINATOR] Revising the existing outline...")

        plan = revise_plan(
            existing_plan=plan,
            feedback=feedback
        )

        print("\n" + "=" * 70)
        print("REVISED INTERNSHIP APPLICATION OUTLINE")
        print("=" * 70)

        print(plan)


def save_final_outline(plan):
    choice = input(
        "\nSave the final outline? (yes/no): "
    ).strip().lower()

    if choice in ("yes", "y"):
        file_path = save_plan(plan)

        print("\n[COORDINATOR] Outline saved successfully.")
        print(f"Saved location: {file_path}")

    else:
        print("\nOutline was not saved.")


def main():
    display_header()

    try:
        # Step 1: Receive free-text request
        student_request = get_student_request()

        # Step 2: Clarify request
        answers = clarification_stage(student_request)

        # Step 3: Propose structured outline
        plan = planning_stage(
            student_request,
            answers
        )

        # Step 4: Revise until the student is satisfied
        final_plan = revision_stage(plan)

        # Step 5: Save the editable outline
        save_final_outline(final_plan)

        print("\n" + "=" * 70)
        print("LAB 1 EXECUTION COMPLETED")
        print("=" * 70)

    except KeyboardInterrupt:
        print("\n\nApplication interrupted by the user.")

    except Exception as error:
        print(f"\n[ERROR] {error}")


if __name__ == "__main__":
    main()
