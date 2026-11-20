
def generate_test_plan(requirement_result, code_result):
    """Generate test scenarios from requirements and generated code."""

    if requirement_result.get("status") != "completed":
        raise ValueError("Requirement analysis is required.")

    if code_result.get("status") != "completed":
        raise ValueError("Code generation is required.")

    test_cases = [
        {
            "test_id": "TC001",
            "test_name": "Application startup",
            "objective": "Verify that the application starts correctly.",
            "expected_result": "Application starts without errors.",
            "priority": "High"
        },
        {
            "test_id": "TC002",
            "test_name": "Valid input handling",
            "objective": "Verify that valid user input is processed.",
            "expected_result": "Input is processed successfully.",
            "priority": "High"
        },
        {
            "test_id": "TC003",
            "test_name": "Invalid input handling",
            "objective": "Verify that invalid input is handled safely.",
            "expected_result": "A meaningful error is returned.",
            "priority": "High"
        },
        {
            "test_id": "TC004",
            "test_name": "Application response",
            "objective": "Verify that application operations return results.",
            "expected_result": "A valid response is generated.",
            "priority": "Medium"
        }
    ]

    for index, requirement in enumerate(
        requirement_result["functional_requirements"],
        start=1
    ):
        test_cases.append({
            "test_id": f"TC{index + 4:03d}",
            "test_name": f"Requirement verification {index}",
            "objective": f"Verify requirement: {requirement}",
            "expected_result": "Requirement is satisfied.",
            "priority": "Medium"
        })

    return {
        "agent": "Testing Agent",
        "status": "completed",
        "testing_approach": "Requirement-based testing",
        "test_cases": test_cases,
        "total_test_cases": len(test_cases)
    }
