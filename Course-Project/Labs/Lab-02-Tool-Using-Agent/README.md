
# Lab 2 – Tool-Using Agent

## 1. Overview

This lab demonstrates the implementation of a tool-using AI agent for an Internship Application and Tracking Portal.

The agent uses Google's Gemini API and Python functions to retrieve student profiles, internship opportunities, and evaluate eligibility.

When the Gemini API quota is unavailable, the application supports local execution using the same Python tools and JSON data.

## 2. Objectives

- Understand tool-using AI agents.
- Implement function calling using Gemini.
- Connect an LLM with external Python functions.
- Retrieve structured information from JSON files.
- Perform internship eligibility checks.
- Handle API errors and provide local fallback execution.

## 3. Technologies Used

- Python 3.12
- Google Gemini API
- Google Gen AI SDK
- Pydantic
- Streamlit
- Pytest
- JSON

## 4. Project Structure

```text
Lab-02-Tool-Using-Agent/
│
├── app/
│   ├── __init__.py
│   ├── schemas.py
│   ├── tools.py
│   └── agent.py
│
├── data/
│   ├── student_profiles.json
│   ├── opportunities.json
│   └── eligibility_rules.json
│
├── tests/
│   ├── test_tools.py
│   └── test_agent.py
│
├── outputs/
├── main.py
├── streamlit_app.py
├── requirements.txt
└── README.md
```

## 5. Available Tools

| Tool | Function |
|---|---|
| read_student_profile | Retrieves student information |
| read_opportunity | Retrieves internship information |
| check_eligibility | Evaluates internship eligibility |

## 6. Working Methodology

1. The user submits a query.
2. Gemini identifies the required function.
3. The agent invokes the corresponding Python tool.
4. The Python function retrieves information from JSON files.
5. The tool result is returned to Gemini.
6. Gemini generates a response for the user.

If the Gemini API quota is exhausted, the application uses local tool execution.

## 7. Eligibility Evaluation

The eligibility engine considers:

- Academic year
- CGPA
- Active backlogs
- Completed credits
- Eligible branch
- Required skills
- Internship-specific requirements

Synthetic demonstration records are marked as unverified. They cannot produce official approval to proceed with an application.

## 8. Execution Instructions

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file in the main repository root:

```env
GEMINI_API_KEY=your_api_key
```

Never commit API credentials.

### Run the CLI application

```bash
python main.py
```

### Run the Streamlit application

```bash
streamlit run streamlit_app.py
```

### Run tests

```bash
python -m pytest tests -v
```

## 9. Testing

The lab includes 12 automated tests:

- 10 tests for data retrieval and eligibility tools.
- 2 tests for agent integration and responses.

Latest recorded test result: 12 tests passed.

## 10. Demonstration Data

The student profiles, internship opportunities, and eligibility rules are synthetic records created for demonstration purposes only. They are not official institutional records or approved internship opportunities.

## 11. Conclusion

This lab demonstrates how an AI agent can use function calling to interact with external Python tools and structured data. It combines LLM-based reasoning, deterministic tool execution, eligibility evaluation, and a Streamlit interface to demonstrate a practical tool-using agent.
