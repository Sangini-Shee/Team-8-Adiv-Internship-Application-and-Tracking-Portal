# Lab 06 – Agent Runtime

## 1. Overview
This lab implements a reusable Agent Runtime for the Internship Application and Tracking Portal. The runtime manages tool registration, task execution, execution history, error handling, and execution limits.

## 2. Objectives
- Implement a reusable agent runtime.
- Register and manage agent tools.
- Execute tasks using registered tools.
- Maintain execution history.
- Handle invalid tools and execution errors.
- Apply execution limits to prevent excessive tool calls.

## 3. Technologies Used
- Python 3.12
- Pytest
- Datetime
- Object-Oriented Programming

## 4. Project Structure

```text
Lab-06-Agent-Runtime/
├── runtime/
│   ├── __init__.py
│   ├── agent_runtime.py
│   ├── execution_engine.py
│   └── tool_manager.py
├── tests/
│   └── test_runtime.py
├── outputs/
├── main.py
├── requirements.txt
└── README.md
```

## 5. Architecture

The runtime consists of three main components:

### Tool Manager
Registers tools, lists available tools, and executes the selected tool.

### Execution Engine
Controls tool execution, maintains execution history, records timestamps, handles errors, and enforces maximum execution steps.

### Agent Runtime
Provides the main interface for registering tools, accepting tasks, executing tools, and retrieving execution history.

## 6. Execution Workflow

1. Initialize the Agent Runtime.
2. Register the required tools.
3. Display the available tools.
4. Accept a task and its arguments.
5. Execute the selected tool.
6. Capture the execution result or error.
7. Record execution details in history.

## 7. Execution

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## 8. Testing

Run automated tests:

```bash
python -m pytest -v
```

**Result: All 7 tests passed.**

Test cases cover:
- Tool registration
- Successful agent execution
- Execution history
- Invalid tool handling
- Empty task validation
- Maximum execution limit
- Invalid tool registration

## 9. Outcome

Successfully implemented a reusable Agent Runtime with modular tool management, controlled execution, error handling, and execution history for the Internship Application and Tracking Portal.

## 10. Limitations

The current implementation uses a demonstration student lookup tool. Integration with the complete MCP server and production internship database remains a future enhancement.
