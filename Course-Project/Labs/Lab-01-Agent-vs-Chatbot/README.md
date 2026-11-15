
# Lab 1 - Agent vs Chatbot

## Project
Internship Application and Tracking Portal

## Objective
To implement an interactive Internship Application Planning
Agent that follows an iterative clarify-plan-revise workflow.

## Problem Context
Students need a structured approach to preparing and tracking
internship applications. A one-shot chatbot response is not
sufficient because internship requirements may be incomplete
and the proposed plan may need revisions.

## Agent Workflow

### 1. Clarification
The Coordinator analyzes the student's free-text request
and asks relevant questions to identify missing information.

### 2. Planning
The Coordinator proposes a structured, editable internship
application outline based on the clarified requirements.

### 3. Revision
The Coordinator revises the existing outline using student
feedback while preserving valid information.

## Technology Stack
- Python 3.12
- Google Gemini API
- Google GenAI SDK
- python-dotenv
- Pytest

## Project Structure

- app/agent.py: Coordinator logic and Gemini integration
- app/prompts.py: Clarification, planning and revision prompts
- tests/test_agent.py: Automated tests
- main.py: Interactive command-line application
- outputs/: Saved internship application outlines

## Configuration

Create a `.env` file in the repository root:

    GEMINI_API_KEY=YOUR_API_KEY
    GEMINI_MODEL=gemini-2.5-flash

Never commit the `.env` file.

## Installation

From the repository root:

    python -m pip install -r Course-Project/Labs/Lab-01-Agent-vs-Chatbot/requirements.txt

## Execution

Navigate to the Lab 1 directory:

    cd Course-Project/Labs/Lab-01-Agent-vs-Chatbot

Run:

    python main.py

## Testing

    python -m pytest tests -v

## Acceptance Criteria

- A vague request produces at least two clarification questions.
- The agent generates a coherent internship application outline.
- The outline is editable.
- The agent revises the existing outline based on feedback.
- The final outline can be saved as a Markdown file.

## Implementation Note

This implementation uses a Python command-line interface
instead of a Jupyter notebook while preserving the Lab 1
clarification, planning and revision workflow.

## Execution Results

The application was successfully executed using the
Google Gemini API.

The following stages were demonstrated:

1. Clarification of student requirements.
2. Generation of an editable internship application outline.
3. Revision based on student feedback.
4. Saving the final outline in Markdown format.

## Testing

Automated tests were executed using Pytest.

Test coverage includes clarification, planning, revision,
input validation and output saving.
