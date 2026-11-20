class AcademicAgent:

    def analyze(self, student, internship):
        cgpa = float(student.get("cgpa", 0))
        backlogs = int(student.get("backlogs", 0))
        credits = int(student.get("credits_completed", 0))

        min_cgpa = float(internship.get("min_cgpa", 0))
        max_backlogs = int(internship.get("max_backlogs", 999))
        min_credits = int(internship.get("min_credits", 0))

        checks = {
            "cgpa": cgpa >= min_cgpa,
            "backlogs": backlogs <= max_backlogs,
            "credits": credits >= min_credits
        }

        return {
            "agent": "Academic Agent",
            "eligible": all(checks.values()),
            "checks": checks,
            "details": {
                "student_cgpa": cgpa,
                "required_cgpa": min_cgpa,
                "student_backlogs": backlogs,
                "maximum_backlogs": max_backlogs,
                "completed_credits": credits,
                "required_credits": min_credits
            }
        }