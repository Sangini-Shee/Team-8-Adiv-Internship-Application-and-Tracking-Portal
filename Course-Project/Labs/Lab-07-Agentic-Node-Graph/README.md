# Lab 07 – Agentic Node Graph

## 1. Overview
This lab implements a stateful agentic workflow using LangGraph for the Internship Application and Tracking Portal. The workflow consists of multiple connected nodes that retrieve student information, fetch internship opportunities, generate skill-based recommendations, and finalize the workflow.

## 2. Objectives
- Understand graph-based agent architecture.
- Implement state management using TypedDict.
- Create reusable workflow nodes.
- Connect nodes using LangGraph.
- Implement conditional routing.
- Generate internship recommendations based on student skills.

## 3. Technologies Used
- Python 3.12
- LangGraph
- LangChain Core
- Pytest
- JSON

## 4. Project Structure

```text
Lab-07-Agentic-Node-Graph/
├── graph/
│   ├── __init__.py
│   ├── state.py
│   ├── nodes.py
│   └── workflow.py
├── tests/
│   └── test_workflow.py
├── outputs/
├── main.py
├── requirements.txt
└── README.md
```

## 5. Architecture

The workflow contains four primary nodes:

1. **Retrieve Student:** Loads the student profile using the student ID.
2. **Retrieve Opportunities:** Loads available internship opportunities.
3. **Recommend Opportunities:** Matches student skills against internship requirements.
4. **Finalize:** Completes the workflow or reports failure.

Conditional edges determine whether the workflow proceeds or terminates when required information is unavailable.

## 6. Workflow Execution

1. Accept the student ID.
2. Retrieve the student profile.
3. Validate the student information.
4. Retrieve internship opportunities.
5. Match student skills with required skills.
6. Sort recommendations by the number of matched skills.
7. Return the workflow result.

## 7. Execution

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

Enter a valid student ID, such as `STU001`.

## 8. Testing

Run:

```bash
python -m pytest -v
```

**Result: All 5 tests passed.**

Test cases include:
- Successful workflow execution
- Recommendation generation
- Invalid student handling
- Empty student ID validation
- No matching opportunities

## 9. Outcome

Successfully implemented a stateful, graph-based agent workflow using LangGraph for student information retrieval and internship recommendations.

## 10. Limitations

The current workflow uses local JSON datasets and skill-overlap matching. It does not yet perform semantic matching or official institutional eligibility verification.
