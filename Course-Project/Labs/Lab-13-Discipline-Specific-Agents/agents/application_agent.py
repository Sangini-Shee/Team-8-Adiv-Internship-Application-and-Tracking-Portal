from datetime import datetime


class ApplicationAgent:

    def prepare(self, student, internship, career_result):
        student_id = student.get(
            "student_id",
            student.get("id", "UNKNOWN")
        )

        return {
            "agent": "Application Agent",
            "application_summary": {
                "student_id": student_id,
                "student_name": student.get("name", "Unknown"),
                "internship_id": internship.get(
                    "internship_id", "UNKNOWN"
                ),
                "internship_title": internship.get(
                    "title", "Unknown Internship"
                ),
                "recommendation": career_result["recommendation"],
                "application_status": "Draft - Awaiting Student Submission",
                "created_at": datetime.now().isoformat(timespec="seconds")
            }
        }