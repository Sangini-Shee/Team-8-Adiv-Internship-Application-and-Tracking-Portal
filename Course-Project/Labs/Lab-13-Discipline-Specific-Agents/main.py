import json
from pathlib import Path

from orchestrator.coordinator import DisciplineCoordinator


CURRENT_LAB = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_LAB.parents[1]

DATA_DIR = (
    PROJECT_ROOT
    / "Labs"
    / "Lab-02-Tool-Using-Agent"
    / "data"
)


def load_json(filename):
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_records(data):
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in ("students", "profiles", "internships", "opportunities"):
            if isinstance(data.get(key), list):
                return data[key]

        return list(data.values())

    raise ValueError("Unsupported dataset format")


def main():
    students = get_records(
        load_json("student_profiles.json")
    )

    internships = get_records(
        load_json("opportunities.json")
    )

    if not students or not internships:
        print("No student or internship records found.")
        return

    print("\n======================================")
    print(" DISCIPLINE-SPECIFIC AGENT SYSTEM")
    print("======================================")

    print("\nAvailable Students:")

    for index, student in enumerate(students, start=1):
        print(
            f"{index}. {student.get('name', 'Unknown')} "
            f"(CGPA: {student.get('cgpa', 'N/A')})"
        )

    try:
        student_choice = int(input("\nSelect student number: "))
        student = students[student_choice - 1]

        if student_choice < 1:
            raise IndexError

    except (ValueError, IndexError):
        print("Invalid student selection.")
        return

    print("\nAvailable Internships:")

    for index, internship in enumerate(internships, start=1):
        print(
            f"{index}. {internship.get('title', 'Unknown')} "
            f"({internship.get('company', internship.get('organization', 'Demo Company'))})"
        )

    try:
        internship_choice = int(input("\nSelect internship number: "))
        internship = internships[internship_choice - 1]

        if internship_choice < 1:
            raise IndexError

    except (ValueError, IndexError):
        print("Invalid internship selection.")
        return

    coordinator = DisciplineCoordinator()

    result = coordinator.analyze_application(
        student,
        internship
    )

    output_file = coordinator.save_result(result)

    print("\n======================================")
    print("          ANALYSIS RESULTS")
    print("======================================")

    print("\nStudent:", result["student"])
    print("Internship:", result["internship"])

    print("\n1. ACADEMIC AGENT")
    academic = result["academic_analysis"]

    print("Academic Eligible:", academic["eligible"])
    print("Academic Checks:", academic["checks"])

    print("\n2. SKILLS AGENT")
    skills = result["skills_analysis"]

    print("Matched Skills:", skills["matched_skills"])
    print("Missing Skills:", skills["missing_skills"])
    print("Skill Match:", skills["match_percentage"], "%")

    print("\n3. CAREER AGENT")
    career = result["career_recommendation"]

    print("Recommendation:", career["recommendation"])

    print("\n4. APPLICATION AGENT")
    application = result["application_preparation"]

    print("Application Summary:")
    print(application["application_summary"])

    print("\n======================================")
    print("Analysis saved successfully!")
    print("Output:", output_file)
    print("======================================")


if __name__ == "__main__":
    main()