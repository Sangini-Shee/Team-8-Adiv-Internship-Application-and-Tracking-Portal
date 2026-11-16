# Lab 09 – Grounding and Evidence

## Overview

This lab implements an evidence-grounded internship recommendation system. The system retrieves student and internship information from structured datasets, generates claims based on the retrieved records, and verifies those claims against their original evidence.

The objective is to reduce unsupported statements and improve the reliability and traceability of agent-generated information.

## Objectives

- Retrieve information from structured data sources.
- Generate evidence-backed claims.
- Associate claims with unique evidence identifiers.
- Verify claims against retrieved records.
- Detect unsupported claims.
- Assign confidence levels to verified results.

## Architecture

```text
             Student ID Input
                    |
                    v
             Evidence Retriever
                    |
          +---------+---------+
          |                   |
          v                   v
    Student Profile     Internship Data
          |                   |
          +---------+---------+
                    |
                    v
              Claim Generator
                    |
                    v
              Claim Verifier
                    |
          +---------+---------+
          |                   |
          v                   v
     Verified Claims    Unsupported Claims
          |                   |
          +---------+---------+
                    |
                    v
             Confidence Report
                    |
                    v
              JSON Output
```

## Modules

### 1. Evidence Retriever
Retrieves student profiles and internship records and assigns unique source identifiers.

### 2. Claim Verifier
Checks claims against retrieved records. Supports exact field verification and eligibility verification based on CGPA and skills.

### 3. Grounded Agent
Coordinates evidence retrieval, claim generation, verification and confidence assessment.

## Technologies Used

- Python 3.12
- JSON
- Pytest

## Project Structure

```text
Lab-09-Grounding-and-Evidence/
├── grounding/
│   ├── __init__.py
│   ├── evidence_retriever.py
│   ├── claim_verifier.py
│   └── grounded_agent.py
├── tests/
│   ├── conftest.py
│   └── test_grounding.py
├── outputs/
├── main.py
├── requirements.txt
└── README.md
```

## Execution

Run the application:

```bash
python main.py
```

Enter a student ID, such as `STU001`.

## Testing

Execute:

```bash
pytest -v
```

The test suite covers evidence retrieval, invalid student handling, claim generation, exact claim verification, unsupported claim detection, eligibility verification and agent execution.

## Output

The application generates:
- Retrieved evidence records.
- Unique evidence IDs.
- Verified and unsupported claims.
- Confidence levels.
- A JSON report in the outputs directory.

## Limitations

- Uses demonstration student and internship datasets.
- Verification is rule-based.
- Confidence labels represent rule-based verification outcomes, not statistically calibrated probabilities.
- Internship information must be independently verified before real applications.

## Conclusion

The lab demonstrates evidence-grounded agent behaviour by connecting generated claims to retrieved source records and verifying them before presenting results. This improves transparency, traceability and reliability in internship recommendations.