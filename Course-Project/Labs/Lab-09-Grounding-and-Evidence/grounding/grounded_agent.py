
from grounding.evidence_retriever import retrieve_evidence
from grounding.claim_verifier import verify_all_claims


def generate_claims(evidence_records):
    """Generate claims using only retrieved records."""

    claims = []

    student_record = next(
        record for record in evidence_records
        if record["source_type"] == "student_profile"
    )

    student = student_record["content"]

    claims.append({
        "claim_id": "CLAIM-001",
        "type": "exact",
        "claim": f"Student CGPA is {student.get('cgpa')}.",
        "field": "cgpa",
        "expected_value": student.get("cgpa"),
        "evidence_ids": [student_record["source_id"]]
    })

    for index, internship_record in enumerate(
        [
            record for record in evidence_records
            if record["source_type"] == "internship_listing"
        ],
        start=1
    ):
        internship = internship_record["content"]

        title = internship.get("title", "Unknown Internship")
        minimum_cgpa = internship.get("min_cgpa", 0)

        claims.append({
            "claim_id": f"CLAIM-{index + 1:03d}",
            "type": "exact",
            "claim": (
                f"{title} requires a minimum CGPA of "
                f"{minimum_cgpa}."
            ),
            "field": "min_cgpa",
            "expected_value": minimum_cgpa,
            "evidence_ids": [internship_record["source_id"]]
        })

        claims.append({
            "claim_id": f"CLAIM-{index + 101:03d}",
            "type": "eligibility",
            "claim": (
                f"Student eligibility assessment for {title}."
            ),
            "evidence_ids": [
                student_record["source_id"],
                internship_record["source_id"]
            ]
        })

    return claims


def run_grounded_agent(student_id):
    """Run the complete evidence-grounded agent."""

    retrieval_result = retrieve_evidence(student_id)

    if retrieval_result["status"] == "error":
        return {
            "status": "error",
            "message": retrieval_result["message"]
        }

    evidence = retrieval_result["evidence"]

    claims = generate_claims(evidence)

    verified_claims = verify_all_claims(
        claims,
        evidence
    )

    verified_count = sum(
        claim["supported"]
        for claim in verified_claims
    )

    unsupported_count = (
        len(verified_claims) - verified_count
    )

    return {
        "status": "completed",
        "student_id": student_id,
        "evidence_count": len(evidence),
        "total_claims": len(verified_claims),
        "verified_claims": verified_count,
        "unsupported_claims": unsupported_count,
        "evidence": evidence,
        "claims": verified_claims,
        "overall_confidence": (
            "high"
            if unsupported_count == 0 and verified_count > 0
            else "review_required"
        )
    }
