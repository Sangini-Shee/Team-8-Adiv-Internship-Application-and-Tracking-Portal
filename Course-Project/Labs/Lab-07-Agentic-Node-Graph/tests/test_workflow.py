
import graph.nodes as nodes
from graph.workflow import build_workflow


STUDENT_DATA = {
    "students": [
        {
            "student_id": "STU001",
            "name": "Sangini Shee",
            "skills": ["Python", "Machine Learning", "SQL"]
        }
    ]
}

INTERNSHIP_DATA = {
    "opportunities": [
        {
            "internship_id": "INT001",
            "title": "AI/ML Intern",
            "skills": ["Python", "Machine Learning"]
        },
        {
            "internship_id": "INT002",
            "title": "Java Developer",
            "skills": ["Java", "Spring Boot"]
        }
    ]
}


def mock_load_json(filename):
    if filename == "student_profiles.json":
        return STUDENT_DATA

    if filename == "opportunities.json":
        return INTERNSHIP_DATA

    raise FileNotFoundError(filename)


def test_successful_workflow(monkeypatch):
    monkeypatch.setattr(nodes, "load_json", mock_load_json)

    graph = build_workflow()
    result = graph.invoke({"student_id": "STU001"})

    assert result["status"] == "completed"
    assert result["student"]["name"] == "Sangini Shee"


def test_recommendations_generated(monkeypatch):
    monkeypatch.setattr(nodes, "load_json", mock_load_json)

    graph = build_workflow()
    result = graph.invoke({"student_id": "STU001"})

    assert len(result["recommendations"]) == 1
    assert result["recommendations"][0]["internship"]["internship_id"] == "INT001"


def test_invalid_student(monkeypatch):
    monkeypatch.setattr(nodes, "load_json", mock_load_json)

    graph = build_workflow()
    result = graph.invoke({"student_id": "STU999"})

    assert result["status"] == "failed"
    assert "not found" in result["error"]


def test_empty_student_id(monkeypatch):
    monkeypatch.setattr(nodes, "load_json", mock_load_json)

    graph = build_workflow()
    result = graph.invoke({"student_id": ""})

    assert result["status"] == "failed"
    assert "required" in result["error"]


def test_no_matching_opportunities(monkeypatch):
    def no_match_data(filename):
        if filename == "student_profiles.json":
            return {
                "students": [{
                    "student_id": "STU001",
                    "name": "Test Student",
                    "skills": ["Graphic Design"]
                }]
            }

        return {
            "opportunities": [{
                "internship_id": "INT001",
                "title": "Python Developer",
                "skills": ["Python"]
            }]
        }

    monkeypatch.setattr(nodes, "load_json", no_match_data)

    graph = build_workflow()
    result = graph.invoke({"student_id": "STU001"})

    assert result["status"] == "completed"
    assert result["recommendations"] == []
