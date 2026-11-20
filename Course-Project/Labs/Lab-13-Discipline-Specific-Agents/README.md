# Lab 13 - Discipline-Specific Agents

## Objective
To develop specialized AI agents that perform different tasks
within an Internship Application and Tracking Portal.

## Agents

1. Academic Agent
   - Checks CGPA.
   - Checks backlogs.
   - Checks completed credits.

2. Skills Agent
   - Compares student skills with internship requirements.
   - Identifies missing skills.
   - Calculates skill match percentage.

3. Career Agent
   - Evaluates internship suitability.
   - Generates internship recommendations.

4. Application Agent
   - Prepares an application summary.
   - Records the application status.

5. Coordinator Agent
   - Coordinates all specialized agents.
   - Combines their outputs.
   - Saves the final analysis.

## Architecture

Student Data
     |
     v
Coordinator Agent
     |
     +---- Academic Agent
     |
     +---- Skills Agent
     |
     +---- Career Agent
     |
     +---- Application Agent
     |
     v
Combined Analysis
     |
     v
JSON Output

## Technologies

- Python
- Object-Oriented Programming
- Multi-Agent Architecture
- JSON
- Pytest

## Execution

Run:

    python main.py

## Testing

Run:

    python -m pytest -v

## Note

This implementation uses local rule-based agents and demo data.
Recommendations are preliminary and do not constitute official
internship eligibility or approval.