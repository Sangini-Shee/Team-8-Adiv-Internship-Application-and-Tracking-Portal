class CareerAgent:

    def recommend(self, academic_result, skills_result, internship):
        academic_eligible = academic_result["eligible"]
        skills_match = skills_result["match_percentage"]

        if academic_eligible and skills_match >= 50:
            recommendation = "Recommended"
        elif academic_eligible and skills_match > 0:
            recommendation = "Consider after skill improvement"
        elif academic_eligible:
            recommendation = "Eligible academically; develop required skills"
        else:
            recommendation = "Not eligible"

        return {
            "agent": "Career Agent",
            "internship_id": internship.get("internship_id", "UNKNOWN"),
            "internship_title": internship.get("title", "Unknown Internship"),
            "recommendation": recommendation,
            "academic_eligible": academic_eligible,
            "skill_match_percentage": skills_match
        }