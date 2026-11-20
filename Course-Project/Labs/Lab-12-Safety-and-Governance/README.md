# Lab 12 – Safety and Governance

## Overview

This lab implements a safety and governance framework for an internship application agent. The system validates inputs, checks generated outputs, enforces predefined policies, requests human approval for sensitive actions and maintains an audit trail.

## Objectives

- Detect suspicious or invalid user inputs.
- Validate generated outputs.
- Enforce organizational policies.
- Require human approval for sensitive actions.
- Maintain an audit trail.
- Improve transparency and accountability.

## Architecture

```text
                 User Input
                     |
                     v
                Input Guard
                     |
                     v
                Policy Engine
                     |
              +------+------+
              |             |
          Normal Action  Sensitive Action
              |             |
              |             v
              |       Human Approval
              |             |
              +------+------+
                     |
                     v
                 Output Guard
                     |
                     v
                Final Decision
                     |
                     v
                 Audit Logger
```

## Modules

### 1. Input Guard
Checks incoming requests for invalid content and suspicious instructions.

### 2. Output Guard
Detects potentially sensitive information, including email addresses, phone numbers and API-key patterns.

### 3. Policy Engine
Evaluates actions against predefined rules and identifies operations requiring human approval.

### 4. Human Approval
Simulates approval or rejection by a human reviewer.

### 5. Audit Logger
Maintains a timestamped record of input validation, policy decisions, approval decisions and output validation.

### 6. Governance Orchestrator
Coordinates all safety and governance components and produces the final decision.

## Technologies Used

- Python 3.12
- Regular Expressions
- JSON
- Python Logging / File I/O
- Pytest

## Project Structure

```text
Lab-12-Safety-and-Governance/
├── safety/
│   ├── __init__.py
│   ├── input_guard.py
│   ├── output_guard.py
│   ├── policy_engine.py
│   ├── human_approval.py
│   └── audit_logger.py
├── governance/
│   ├── __init__.py
│   └── orchestrator.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_safety.py
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

Choose an action, enter a proposed output and follow the human approval prompt if required.

## Testing

Run:

```bash
pytest -v
```

The test suite covers input validation, suspicious instructions, output validation, policy enforcement, human approval, rejection, audit logging and governance workflow execution.

## Output

Audit events are stored in:

`outputs/audit_log.jsonl`

## Limitations

- Safety checks use predefined regular expressions and keyword rules.
- Human approval is simulated through terminal input.
- The audit log is a local file and does not provide tamper-proof storage.
- The implementation is a demonstration framework, not a complete production security system.

## Conclusion

The lab demonstrates a governance framework that introduces input and output validation, policy enforcement, human oversight and audit logging into an agent workflow. These mechanisms help make agent operations more controlled, transparent and accountable.