
import asyncio

from grounding.evidence_retriever import retrieve_evidence
from grounding.claim_verifier import verify_claim, verify_all_claims
from grounding.grounded_agent import (
    generate_claims,
    run_grounded_agent
)


def test_evidence_retrieval():
    result = retrieve_evidence("STU001")

    assert result["status"] == "success"
    assert result["evidence_count"] >= 2


def test_student_evidence_exists():
    result = retrieve_evidence("STU001")

    student_evidence = [
        item for item in result["evidence"]
        if item["source_type"] == "student_profile"
    ]

    assert len(student_evidence) == 1
    assert student_evidence[0]["content"]["cgpa"] == 8.4


def test_invalid_student():
    result = retrieve_evidence("INVALID")

    assert result["status"] == "error"
    assert result["evidence"] == []


def test_claim_generation():
    result = retrieve_evidence("STU001")
    claims = generate_claims(result["evidence"])

    assert len(claims) >= 3
    assert all("evidence_ids" in claim for claim in claims)


def test_exact_claim_verification():
    result = retrieve_evidence("STU001")

    student_record = next(
        item for item in result["evidence"]
        if item["source_type"] == "student_profile"
    )

    claim = {
        "claim_id": "TEST-001",
        "type": "exact",
        "claim": "Student CGPA is 8.4",
        "field": "cgpa",
        "expected_value": 8.4,
        "evidence_ids": [student_record["source_id"]]
    }

    verified = verify_claim(claim, result["evidence"])

    assert verified["supported"] is True
    assert verified["verification_status"] == "verified"


def test_unsupported_claim_detection():
    result = retrieve_evidence("STU001")

    student_record = next(
        item for item in result["evidence"]
        if item["source_type"] == "student_profile"
    )

    claim = {
        "claim_id": "TEST-002",
        "type": "exact",
        "claim": "Student CGPA is 10.0",
        "field": "cgpa",
        "expected_value": 10.0,
        "evidence_ids": [student_record["source_id"]]
    }

    verified = verify_claim(claim, result["evidence"])

    assert verified["supported"] is False
    assert verified["verification_status"] == "unsupported"


def test_eligibility_claim_verification():
    result = retrieve_evidence("STU001")
    claims = generate_claims(result["evidence"])

    eligibility_claims = [
        claim for claim in claims
        if claim["type"] == "eligibility"
    ]

    verified = verify_all_claims(
        eligibility_claims,
        result["evidence"]
    )

    assert len(verified) >= 1
    assert all(
        claim["verification_status"] in
        ["verified", "unsupported"]
        for claim in verified
    )


def test_grounded_agent_execution():
    result = run_grounded_agent("STU001")

    assert result["status"] == "completed"
    assert result["evidence_count"] >= 2
    assert result["total_claims"] >= 1


def test_grounded_agent_invalid_student():
    result = run_grounded_agent("INVALID")

    assert result["status"] == "error"


def test_evidence_ids_are_unique():
    result = retrieve_evidence("STU001")

    source_ids = [
        item["source_id"]
        for item in result["evidence"]
    ]

    assert len(source_ids) == len(set(source_ids))
