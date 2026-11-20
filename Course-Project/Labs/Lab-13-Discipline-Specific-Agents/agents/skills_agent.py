class SkillsAgent:

    def analyze(self, student, internship):
        student_skills = {
            skill.lower()
            for skill in student.get("skills", [])
        }

        required_skills = {
            skill.lower()
            for skill in internship.get("required_skills", [])
        }

        matched = sorted(student_skills.intersection(required_skills))
        missing = sorted(required_skills - student_skills)

        match_percentage = (
            len(matched) / len(required_skills) * 100
            if required_skills else 100
        )

        return {
            "agent": "Skills Agent",
            "matched_skills": matched,
            "missing_skills": missing,
            "match_percentage": round(match_percentage, 2),
            "suitable": len(missing) == 0
        }