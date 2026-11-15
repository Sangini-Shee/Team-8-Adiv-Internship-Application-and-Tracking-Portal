
import pytest

from app.tools import (
    read_student_profile,
    read_opportunity,
    check_eligibility
)


def test_read_sangini_profile():
    student = read_student_profile("STU001")

    assert student.full_name == "Sangini Shee"
    assert student.cgpa == 8.4
    assert student.active_backlogs == 0


def test_read_sindhu_profile():
    student = read_student_profile("STU002")

    assert student.full_name == "K Sindhu"
    assert student.cgpa == 7.6


def test_read_chirag_profile():
    student = read_student_profile("STU003")

    assert student.full_name == "Chirag Hanamaratti"
    assert student.active_backlogs == 1


def test_read_kshitij_profile():
    student = read_student_profile("STU004")

    assert student.full_name == "Kshitij Heblikar"
    assert student.cgpa == 7.0


def test_read_opportunity():
    opportunity = read_opportunity("INT001")

    assert opportunity.title == "AI and Machine Learning Intern"
    assert opportunity.min_cgpa == 7.0


def test_invalid_student_id():
    with pytest.raises(ValueError):
        read_student_profile("INVALID")


def test_invalid_opportunity_id():
    with pytest.raises(ValueError):
        read_opportunity("INVALID")


def test_sangini_eligibility_checks():
    result = check_eligibility("STU001", "INT001")

    assert result.checks["institution_cgpa"] is True
    assert result.checks["institution_backlogs"] is True
    assert result.checks["skills_match"] is True

    # Demo records cannot receive official approval.
    assert result.status == "review_required"
    assert result.can_proceed_to_application is False


def test_chirag_eligibility_checks():
    result = check_eligibility("STU003", "INT001")

    assert result.checks["institution_cgpa"] is False
    assert result.checks["institution_backlogs"] is False
    assert result.status == "review_required"


def test_invalid_eligibility_request():
    with pytest.raises(ValueError):
        check_eligibility("INVALID", "INT001")
