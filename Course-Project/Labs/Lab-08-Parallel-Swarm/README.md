# Lab 08 – Parallel Swarm

## Overview
This lab demonstrates a parallel multi-agent system for internship recommendation and student analysis. Three specialized agents execute concurrently and their results are combined by a central swarm orchestrator.

## Objectives
- Implement multiple specialized agents.
- Execute agents concurrently using Python asyncio.
- Analyse student academic profiles.
- Match student skills with internship requirements.
- Analyse available internship opportunities.
- Combine agent outputs into a unified result.

## Architecture

```text
                 User Input
                     |
                 Student ID
                     |
              Swarm Orchestrator
                     |
          Parallel Agent Execution
           /          |          \
          /           |           \
 Profile Analyst  Skill Matching  Opportunity
     Agent           Agent        Analyst Agent
          \           |           /
           \          |          /
              Result Aggregation
                     |
              Combined Output
                     |
                JSON Storage
```

## Agents

### 1. Profile Analyst Agent
- Retrieves student information.
- Analyses CGPA and active backlogs.
- Extracts branch and technical skills.
- Generates an academic summary.

### 2. Skill Matching Agent
- Compares student skills with internship requirements.
- Identifies matched and missing skills.
- Calculates skill-match percentages.
- Ranks opportunities based on skill compatibility.

### 3. Opportunity Analyst Agent
- Retrieves available internship listings.
- Analyses company, domain and required skills.
- Identifies minimum CGPA requirements.
- Displays work mode, duration and verification status.

## Parallel Execution
The swarm orchestrator uses Python's `asyncio.gather()` to execute all three agents concurrently.

The agents return their individual results, which are aggregated into a single response.

## Technologies Used
- Python 3.12
- Asyncio
- JSON
- Pytest

## Project Structure

```text
Lab-08-Parallel-Swarm/
├── agents/
│   ├── __init__.py
│   ├── profile_agent.py
│   ├── skill_agent.py
│   └── opportunity_agent.py
├── swarm/
│   ├── __init__.py
│   └── orchestrator.py
├── tests/
│   ├── conftest.py
│   └── test_swarm.py
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

Enter a student ID, for example:

```text
STU001
```

## Testing

Run:

```bash
pytest -v
```

**Test result: 8 tests passed.**

## Output
The application displays:
- Student profile analysis.
- Skill matching results.
- Internship opportunity analysis.
- Combined swarm execution status.

The combined results are saved in the `outputs/` directory as a JSON file.

## Limitations
- Uses demonstration student and internship data from Lab 2.
- Agent analysis is rule-based and does not require an external LLM.
- Internship listings require independent verification before real applications.

## Conclusion
The lab successfully demonstrates parallel multi-agent orchestration. Specialized agents independently analyse student profiles, skills and internship opportunities, while the swarm orchestrator combines their outputs into a unified result.