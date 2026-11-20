import pytest
from db import init_db, seed_data, get_conn
from workflow import review_application

def test_coordinator_cannot_review_before_hod():
    init_db()
    seed_data()
    with get_conn() as c:
        student = c.execute("SELECT student_id FROM students LIMIT 1").fetchone()["student_id"]
        internship = c.execute("SELECT id FROM internships LIMIT 1").fetchone()["id"]
        c.execute("DELETE FROM applications WHERE student_id=? AND internship_id=?", (student, internship))
        c.execute("INSERT INTO applications(student_id, internship_id) VALUES(?,?)", (student, internship))
        app_id = c.execute("SELECT id FROM applications WHERE student_id=? AND internship_id=?", (student, internship)).fetchone()["id"]
    with pytest.raises(ValueError):
        review_application(app_id, "Coordinator", "Approved", "test-coordinator")
    with get_conn() as c:
        c.execute("DELETE FROM applications WHERE id=?", (app_id,))


def test_hod_then_internship_head_can_approve():
    init_db()
    seed_data()
    with get_conn() as c:
        student = c.execute("SELECT student_id FROM students WHERE student_id='STU001'").fetchone()["student_id"]
        internship = c.execute("SELECT id FROM internships ORDER BY id LIMIT 1").fetchone()["id"]
        c.execute("DELETE FROM applications WHERE student_id=? AND internship_id=?", (student, internship))
        c.execute("INSERT INTO applications(student_id, internship_id) VALUES(?,?)", (student, internship))
        app_id = c.execute(
            "SELECT id FROM applications WHERE student_id=? AND internship_id=?",
            (student, internship)
        ).fetchone()["id"]
    assert review_application(app_id, "HOD", "Approved", "test-hod") == "Awaiting Internship Head Approval"
    assert review_application(app_id, "Internship Head", "Approved", "test-head") == "Approved"
    with get_conn() as c:
        c.execute("DELETE FROM applications WHERE id=?", (app_id,))
