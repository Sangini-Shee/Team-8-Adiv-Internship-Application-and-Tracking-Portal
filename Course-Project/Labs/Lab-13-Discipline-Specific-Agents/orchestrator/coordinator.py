import json
from pathlib import Path

from agents.academic_agent import AcademicAgent
from agents.skills_agent import SkillsAgent
from agents.career_agent import CareerAgent
from agents.application_agent import ApplicationAgent


class DisciplineCoordinator:

    def __init__(self):
        self.academic_agent = AcademicAgent()
        self.skills_agent = SkillsAgent()
        self.career_agent = CareerAgent()
        self.application_agent = ApplicationAgent()

    def analyze_application(self, student, internship):

        academic_result = self.academic_agent.analyze(
            student, internship
        )

        skills_result = self.skills_agent.analyze(
            student, internship
        )

        career_result = self.career_agent.recommend(
            academic_result,
            skills_result,
            internship
        )

        application_result = self.application_agent.prepare(
            student,
            internship,
            career_result
        )

        return {
            "student": student.get("name", "Unknown"),
            "internship": internship.get("title", "Unknown"),
            "academic_analysis": academic_result,
            "skills_analysis": skills_result,
            "career_recommendation": career_result,
            "application_preparation": application_result
        }

    def save_result(self, result, output_dir="outputs"):

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        student_name = result["student"].replace(" ", "_")
        file_path = output_path / f"{student_name}_analysis.json"

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4)

        return file_path