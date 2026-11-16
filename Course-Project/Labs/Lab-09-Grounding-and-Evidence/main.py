
import json
from pathlib import Path

from grounding.grounded_agent import run_grounded_agent


def main():
    print("=" * 65)
    print("       INTERNSHIP GROUNDING AND EVIDENCE SYSTEM")
    print("=" * 65)

    student_id = input(
        "\nEnter Student ID (e.g., STU001): "
    ).strip()

    if not student_id:
        print("Error: Student ID cannot be empty.")
        return

    try:
        result = run_grounded_agent(student_id)

        if result["status"] == "error":
            print(f"\nError: {result['message']}")
            return

        print("\n" + "=" * 65)
        print("                  GROUNDING RESULTS")
        print("=" * 65)

        print(f"\nStudent ID: {result['student_id']}")
        print(f"Evidence Records: {result['evidence_count']}")
        print(f"Total Claims: {result['total_claims']}")
        print(f"Verified Claims: {result['verified_claims']}")
        print(f"Unsupported Claims: {result['unsupported_claims']}")
        print(f"Overall Confidence: {result['overall_confidence']}")

        print("\n" + "-" * 65)
        print("                 CLAIM VERIFICATION")
        print("-" * 65)

        for claim in result["claims"]:
            print(f"\nClaim ID: {claim['claim_id']}")
            print(f"Claim: {claim['claim']}")
            print(f"Status: {claim['verification_status']}")
            print(f"Confidence: {claim['confidence']}")
            print(f"Reason: {claim['reason']}")
            print(f"Evidence IDs: {claim['evidence_ids']}")

            if "matched_skills" in claim:
                print(f"Matched Skills: {claim['matched_skills']}")

        output_dir = Path(__file__).resolve().parent / "outputs"
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / f"{student_id}_grounding_results.json"

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4, default=str)

        print("\n" + "-" * 65)
        print(f"Full results saved to: {output_file}")
        print("-" * 65)

    except Exception as error:
        print(f"\nExecution failed: {error}")


if __name__ == "__main__":
    main()
