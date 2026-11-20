from agents import assess_eligibility, recommend

def student():
    return {
        "student_id": "STU001",
        "full_name": "Demo Student",
        "department": "CS-AI",
        "cgpa": 8.4,
        "backlogs": 0,
        "credits": 150,
        "skills": "Python, ML, SQL"
    }

def internship():
    return {
        "id": 1,
        "title": "AI/ML Intern",
        "company": "Demo Company",
        "required_skills": "Python, ML",
        "min_cgpa": 7.0,
        "max_backlogs": 0,
        "min_credits": 140
    }

def test_eligible_student_passes():
    result = assess_eligibility(student(), internship())
    assert result["eligible"] is True
    assert result["skill_match"] == 100.0

def test_cgpa_requirement_fails():
    s = student()
    s["cgpa"] = 5.5
    result = assess_eligibility(s, internship())
    assert result["eligible"] is False
    assert result["checks"]["CGPA requirement"] is False

def test_backlog_requirement_fails():
    s = student()
    s["backlogs"] = 2
    result = assess_eligibility(s, internship())
    assert result["checks"]["Backlog requirement"] is False

def test_missing_skills_are_reported():
    s = student()
    s["skills"] = "Python"
    result = assess_eligibility(s, internship())
    assert result["missing_skills"] == ["ml"]
    assert result["skill_match"] == 50.0

def test_recommendations_rank_eligible_first():
    s = student()
    opportunities = [
        internship(),
        {**internship(), "id": 2, "title": "Not eligible", "min_cgpa": 9.5}
    ]
    result = recommend(s, opportunities)
    assert result[0]["title"] == "AI/ML Intern"
    assert result[0]["eligible"] is True
    assert result[1]["eligible"] is False
