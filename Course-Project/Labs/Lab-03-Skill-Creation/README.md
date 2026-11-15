
# Lab 3 – Skill Creation

## 1. Overview

This lab demonstrates the creation of reusable, schema-typed skills for an AI-powered Internship Application and Tracking Portal.

Each skill packages related operations into an independent workflow that can be reused by different agents and application modules.

## 2. Objectives

- Understand reusable AI skills.
- Create typed skill input and output schemas.
- Implement reusable Python skill modules.
- Register and retrieve skills through a skill registry.
- Integrate skills with existing Python tools and JSON resources.

## 3. Technologies Used

- Python
- Pydantic
- Streamlit
- JSON
- Pytest

## 4. Implemented Skills

| Skill | Purpose |
|---|---|
| Opportunity Discovery | Finds internship opportunities matching student preferences and skills. |
| Eligibility Verification | Checks academic and internship-specific eligibility requirements. |
| Application Preparation | Creates an application preparation checklist and readiness status. |

## 5. Architecture

1. User selects a skill.
2. The skill receives validated structured input.
3. The skill accesses the required data resources.
4. It executes its workflow.
5. A structured output is returned.

## 6. Project Structure

```text
Lab-03-Skill-Creation/
├── app/
│   ├── __init__.py
│   ├── schemas.py
│   ├── skill_registry.py
│   └── skills.py
├── tests/
│   └── test_skills.py
├── outputs/
├── main.py
├── streamlit_app.py
├── requirements.txt
└── README.md
```

## 7. Execution

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the CLI:

```bash
python main.py
```

Run the Skill Center:

```bash
streamlit run streamlit_app.py
```

Run tests:

```bash
python -m pytest tests -v
```

## 8. Testing

Six automated tests cover skill registration, skill retrieval, opportunity discovery, eligibility verification, application preparation, and invalid student handling.

Latest recorded result: 6 tests passed.

## 9. Conclusion

This lab demonstrates how reusable, schema-typed skills can package repeatable capabilities into independent workflows. These skills can be integrated into the larger Internship Application and Tracking Portal.
