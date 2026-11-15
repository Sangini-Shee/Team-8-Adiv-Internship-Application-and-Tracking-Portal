
from app.agent import run_agent


def test_agent_reads_student_profile():
    response = run_agent(
        "Retrieve the student profile for STU001. "
        "Use the read_student_profile tool."
    )

    print("\nAgent response:", response)

    assert response
    assert "Sangini Shee" in response
    assert "STU001" in response


def test_agent_checks_internship_eligibility():
    response = run_agent(
        "Check whether student STU001 is eligible for internship INT001. "
        "Use the check_eligibility tool and explain the result."
    )

    print("\nAgent response:", response)

    assert response
    assert "official verification" in response.lower()
    assert "cannot officially proceed" in response.lower()
