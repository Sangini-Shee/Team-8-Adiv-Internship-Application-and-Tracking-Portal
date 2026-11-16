
def verify_claim(claim, evidence_records):
    """
    Verify a claim against retrieved evidence.

    Supported verification types:
    1. exact: Checks whether a field matches an expected value.
    2. eligibility: Checks CGPA and skill requirements using
       student and internship evidence.
    """

    evidence_map = {
        record["source_id"]: record
        for record in evidence_records
    }

    evidence_ids = claim.get("evidence_ids", [])

    selected_evidence = [
        evidence_map[source_id]
        for source_id in evidence_ids
        if source_id in evidence_map
    ]

    if not selected_evidence or len(selected_evidence) != len(evidence_ids):
        return {
            **claim,
            "supported": False,
            "verification_status": "unsupported",
            "confidence": "low",
            "reason": "Required evidence was not found."
        }

    claim_type = claim.get("type")

    if claim_type == "exact":
        field = claim.get("field")
        expected_value = claim.get("expected_value")

        supported = any(
            record["content"].get(field) == expected_value
            for record in selected_evidence
        )

        return {
            **claim,
            "supported": supported,
            "verification_status": (
                "verified" if supported else "unsupported"
            ),
            "confidence": "high" if supported else "low",
            "reason": (
                "Claim matches the retrieved source."
                if supported
                else "Claim does not match the retrieved source."
            )
        }

    if claim_type == "eligibility":
        student_record = next(
            (
                record for record in selected_evidence
                if record["source_type"] == "student_profile"
            ),
            None
        )

        internship_record = next(
            (
                record for record in selected_evidence
                if record["source_type"] == "internship_listing"
            ),
            None
        )

        if not student_record or not internship_record:
            return {
                **claim,
                "supported": False,
                "verification_status": "unsupported",
                "confidence": "low",
                "reason": "Student or internship evidence is missing."
            }

        student = student_record["content"]
        internship = internship_record["content"]

        cgpa = float(student.get("cgpa", 0))
        minimum_cgpa = float(internship.get("min_cgpa", 0))

        student_skills = {
            skill.lower()
            for skill in student.get("skills", [])
        }

        required_skills = {
            skill.lower()
            for skill in internship.get(
                "required_skills",
                internship.get("skills", [])
            )
        }

        matched_skills = student_skills.intersection(
            required_skills
        )

        cgpa_met = cgpa >= minimum_cgpa
        skills_met = bool(matched_skills)

        supported = cgpa_met and skills_met

        return {
            **claim,
            "supported": supported,
            "verification_status": (
                "verified" if supported else "unsupported"
            ),
            "confidence": "high" if supported else "low",
            "cgpa_requirement_met": cgpa_met,
            "skill_requirement_met": skills_met,
            "matched_skills": sorted(matched_skills),
            "reason": (
                "Eligibility conditions are supported by the "
                "student and internship records."
                if supported
                else "One or more eligibility conditions are not met."
            )
        }

    return {
        **claim,
        "supported": False,
        "verification_status": "unsupported",
        "confidence": "low",
        "reason": "Unknown claim verification type."
    }


def verify_all_claims(claims, evidence_records):
    """Verify multiple claims against their evidence."""

    return [
        verify_claim(claim, evidence_records)
        for claim in claims
    ]
