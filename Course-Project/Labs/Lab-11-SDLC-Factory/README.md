# Lab 11 – SDLC Factory

## Overview

This lab demonstrates an automated Software Development Life Cycle (SDLC) workflow using multiple specialized agents. The system processes a software project description and generates requirement analysis, system design, source-code skeletons, a testing plan and project documentation.

## Objectives

- Automate requirement analysis.
- Generate a high-level system design.
- Generate a basic source-code skeleton.
- Create test cases from requirements.
- Generate project documentation.
- Coordinate multiple agents through an orchestrator.

## Architecture

```text
               Project Description
                       |
                       v
             Requirement Analysis Agent
                       |
                       v
                  Design Agent
                       |
                       v
              Code Generation Agent
                       |
                       v
                  Testing Agent
                       |
                       v
             Documentation Agent
                       |
                       v
                SDLC Orchestrator
                       |
                       v
                Generated Project
```

## Agents

### 1. Requirement Analysis Agent
Extracts functional and non-functional requirements from the project description.

### 2. Design Agent
Creates a layered architecture and identifies the main system components.

### 3. Code Generation Agent
Generates a basic Python project structure and source-code skeleton.

### 4. Testing Agent
Creates test scenarios based on the extracted requirements.

### 5. Documentation Agent
Generates project documentation containing requirements, architecture, generated files and testing information.

## Technologies Used

- Python 3.12
- JSON
- Pytest
- Python standard library

## Project Structure

```text
Lab-11-SDLC-Factory/
├── agents/
│   ├── __init__.py
│   ├── requirement_agent.py
│   ├── design_agent.py
│   ├── code_agent.py
│   ├── testing_agent.py
│   └── documentation_agent.py
├── factory/
│   ├── __init__.py
│   └── orchestrator.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_factory.py
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

Enter a project name and describe its requirements. Type `END` on a separate line to finish the description.

## Testing

Run:

```bash
pytest -v
```

The test suite covers requirement extraction, design generation, code generation, file creation, test-plan generation, documentation and complete workflow execution.

## Generated Outputs

The application generates:

- Python source-code skeleton.
- Project documentation in Markdown.
- SDLC execution results in JSON.
- Requirement analysis.
- System design.
- Test plan.

Generated artifacts are saved in the `outputs/` directory.

## Limitations

- Uses rule-based requirement extraction rather than an LLM.
- Generates a starter code skeleton, not a complete production application.
- Test cases are generated as a plan; they are not automatically executed against a finished application.
- System design is a high-level layered architecture.

## Conclusion

The lab demonstrates how specialized agents can coordinate to automate major SDLC activities. It provides a structured workflow from project requirements through design, code scaffolding, testing and documentation.