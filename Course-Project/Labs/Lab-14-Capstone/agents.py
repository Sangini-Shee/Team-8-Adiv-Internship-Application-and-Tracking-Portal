def assess_eligibility(student, internship):
    checks = {
        "CGPA requirement": float(student["cgpa"]) >= float(internship["min_cgpa"]),
        "Backlog requirement": int(student["backlogs"]) <= int(internship["max_backlogs"]),
        "Credit requirement": int(student["credits"]) >= int(internship["min_credits"]),
    }
    student_skills = {x.strip().lower() for x in student["skills"].split(",") if x.strip()}
    required = {x.strip().lower() for x in internship["required_skills"].split(",") if x.strip()}
    matched = sorted(student_skills & required)
    missing = sorted(required - student_skills)
    skill_score = round(100 * len(matched) / len(required), 1) if required else 100.0
    return {
        "eligible": all(checks.values()),
        "checks": checks,
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_match": skill_score,
    }

def recommend(student, internships):
    results = []
    for internship in internships:
        result = assess_eligibility(student, internship)
        results.append({**dict(internship), **result})
    return sorted(results, key=lambda x: (x["eligible"], x["skill_match"]), reverse=True)
