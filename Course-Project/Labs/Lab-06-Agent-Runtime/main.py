
from runtime.agent_runtime import AgentRuntime


def sample_student_lookup(student_id):
    students = {
        "STU001": {
            "name": "Sangini Shee",
            "department": "CS-AI",
            "cgpa": 8.4
        },
        "STU002": {
            "name": "K Sindhu",
            "department": "CS-AI",
            "cgpa": 7.6
        }
    }

    return students.get(
        student_id,
        {"error": "Student not found"}
    )


def main():

    runtime = AgentRuntime(max_steps=5)

    runtime.register_tool(
        "student_lookup",
        sample_student_lookup,
        "Retrieve student information using student ID."
    )

    print("\n===== INTERNSHIP PORTAL AGENT RUNTIME =====")

    print("\nAvailable Tools:")
    for tool in runtime.get_available_tools():
        print(f"- {tool['name']}: {tool['description']}")

    task = input("\nEnter your task: ").strip()
    student_id = input("Enter Student ID: ").strip()

    result = runtime.run(
        task=task,
        tool_name="student_lookup",
        arguments={"student_id": student_id}
    )

    print("\n===== EXECUTION RESULT =====")
    print(result)

    print("\n===== EXECUTION HISTORY =====")
    print(runtime.get_execution_history())


if __name__ == "__main__":
    main()
