
from graph.workflow import internship_graph


def main():
    print("\n===== INTERNSHIP AGENTIC NODE GRAPH =====")

    student_id = input("Enter Student ID: ").strip()

    initial_state = {
        "student_id": student_id,
        "messages": []
    }

    result = internship_graph.invoke(initial_state)

    print("\n===== WORKFLOW RESULT =====")
    print("Status:", result.get("status"))

    if result.get("error"):
        print("Error:", result["error"])
        return

    print("\nStudent:")
    print(result.get("student"))

    print("\nRecommended Internships:")

    recommendations = result.get("recommendations", [])

    if not recommendations:
        print("No matching opportunities found.")
    else:
        for item in recommendations:
            internship = item["internship"]
            print("\nInternship:", internship.get("title", internship.get("role", "Not specified")))
            print("Matched Skills:", ", ".join(item["matched_skills"]))
            print("Match Count:", item["match_count"])

    print("\nWorkflow Messages:")
    for message in result.get("messages", []):
        print("-", message)


if __name__ == "__main__":
    main()
