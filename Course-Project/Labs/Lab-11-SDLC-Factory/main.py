
from factory.orchestrator import run_sdlc_factory


def main():
    print("=" * 65)
    print("             AUTOMATED SDLC FACTORY")
    print("=" * 65)

    project_name = input(
        "\nEnter project name: "
    ).strip()

    print("\nDescribe your software project.")
    print("Enter the description in one or more lines.")
    print("Type END on a separate line when finished.\n")

    description_lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        description_lines.append(line)

    project_description = "\n".join(description_lines)

    if not project_name or not project_description.strip():
        print("\nError: Project name and description are required.")
        return

    try:
        result = run_sdlc_factory(
            project_name,
            project_description
        )

        print("\n" + "=" * 65)
        print("                 SDLC FACTORY RESULTS")
        print("=" * 65)

        print(f"\nProject: {result['project_name']}")
        print(f"Status: {result['status']}")
        print(f"Agents Executed: {result['agents_executed']}")

        print(
            "\nFunctional Requirements:",
            len(result["requirement_analysis"]["functional_requirements"])
        )

        print(
            "Non-Functional Requirements:",
            len(result["requirement_analysis"]["non_functional_requirements"])
        )

        print(
            "\nArchitecture:",
            result["system_design"]["architecture"]
        )

        print(
            "Generated Source Files:",
            result["code_generation"]["file_count"]
        )

        print(
            "Generated Test Cases:",
            result["testing_plan"]["total_test_cases"]
        )

        print("\nGenerated Project:")
        print(result["generated_project_path"])

        print("\nDocumentation:")
        print(result["documentation_path"])

        print("\nFull results saved in outputs/sdlc_factory_results.json")

    except Exception as error:
        print(f"\nSDLC execution failed: {error}")


if __name__ == "__main__":
    main()
