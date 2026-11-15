
import json
from pathlib import Path

from swarm.orchestrator import run_swarm


def main():
    print("=" * 60)
    print("       INTERNSHIP PARALLEL AGENT SWARM")
    print("=" * 60)

    student_id = input("\nEnter Student ID (e.g., STU001): ").strip()

    if not student_id:
        print("Error: Student ID cannot be empty.")
        return

    try:
        result = run_swarm(student_id)

        print("\n" + "=" * 60)
        print("                 SWARM RESULTS")
        print("=" * 60)

        print(f"\nOverall Status: {result['status']}")
        print(f"Student ID: {result['student_id']}")

        if result["status"] == "error":
            print("\nErrors:")
            for error in result.get("errors", []):
                print(f"- {error}")
            return

        print(f"Agents Executed: {result['agents_executed']}")
        print(f"Execution Mode: {result['execution_mode']}")

        for agent_name, agent_result in result["agent_results"].items():
            print(f"\n{'-' * 60}")
            print(f"{agent_name.replace('_', ' ').upper()}")
            print("-" * 60)

            if isinstance(agent_result, Exception):
                print(f"Agent failed: {agent_result}")
                continue

            if agent_result.get("status") == "error":
                print(agent_result.get("message", "Agent failed."))
                continue

            print(json.dumps(agent_result, indent=4))

        output_dir = Path(__file__).resolve().parent / "outputs"
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / f"{student_id}_swarm_results.json"

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4, default=str)

        print(f"\nResults saved to: {output_file}")

    except Exception as error:
        print(f"\nSwarm execution failed: {error}")


if __name__ == "__main__":
    main()
