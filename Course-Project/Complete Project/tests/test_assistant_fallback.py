
from db import init_db, seed_data
from assistant_service import answer_student_question

def test_student_assistant_uses_current_head_approval_column():
    init_db()
    seed_data()
    answer = answer_student_question("what internship should i apply for?", "STU001")
    assert isinstance(answer, str)
    assert answer.strip()
    assert "OperationalError" not in answer
    assert "Traceback" not in answer
