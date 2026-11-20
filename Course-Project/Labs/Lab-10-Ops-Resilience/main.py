
import json
from pathlib import Path

from resilience.resilient_agent import (
    process_student,
    simulate_unstable_operation
)


def main():
    print("=" * 65)
    print("           INTERNSHIP OPS RESILIENCE SYSTEM")
    print("=" * 65)

    print("\n1. Process Student")
    print("2. Simulate Temporary Service Failure")
    print("3. Exit")

    choice = input("\nSelect an option: ").strip()

    result = None

    if choice == "1":
        student_id = input(
            "\nEnter Student ID (e.g., STU001): "
        ).strip()

        result = process_student(student_id)

    elif choice == "2":
        result = simulate_unstable_operation(
            failures_before_success=2
        )

    elif choice == "3":
        print("\nExiting application.")
        return

    else:
        print("\nInvalid option. Please select 1, 2 or 3.")
        return

    print("\n" + "=" * 65)
    print("                    EXECUTION RESULT")
    print("=" * 65)

    print(json.dumps(result, indent=4, default=str))

    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "latest_execution.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, default=str)

    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
