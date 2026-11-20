# Lab 10 – Ops Resilience

## Overview

This lab implements an operationally resilient internship agent system. It demonstrates how an agent can handle unexpected failures, retry unsuccessful operations, maintain execution logs and recover safely from errors.

## Objectives

- Implement structured error handling.
- Develop an automatic retry mechanism.
- Maintain application logs.
- Handle temporary service failures.
- Implement fallback responses.
- Improve application fault tolerance.

## Architecture

```text
              User Input
                  |
                  v
             Resilient Agent
                  |
                  v
             Input Validation
                  |
                  v
              Data Loader
                  |
                  v
              Retry Handler
                  |
           +------+------+
           |             |
        Success        Failure
           |             |
           v             v
      Process Data   Recovery Handler
           |             |
           v             v
       Result        Fallback Result
           |             |
           +------+------+
                  |
                  v
              JSON Output
                  |
                  v
             Logging System
```

## Modules

### 1. Logger
Records application events, execution attempts, warnings and errors.

### 2. Retry Handler
Automatically retries failed operations using a configurable number of attempts and delay.

### 3. Recovery Handler
Handles errors and generates fallback responses.

### 4. Resilient Agent
Integrates validation, data loading, retry logic and error recovery.

## Technologies Used

- Python 3.12
- Logging
- JSON
- Pytest

## Project Structure

```text
Lab-10-Ops-Resilience/
├── resilience/
│   ├── __init__.py
│   ├── logger.py
│   ├── retry_handler.py
│   ├── recovery.py
│   └── resilient_agent.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_resilience.py
├── outputs/
├── main.py
├── requirements.txt
└── README.md
```

## Execution

Run:

```bash
python main.py
```

Select option 1 to retrieve a student profile or option 2 to simulate temporary service failures.

## Testing

Run:

```bash
pytest -v
```

The test suite covers successful execution, invalid inputs, fallback recovery, retry success, retry exhaustion and temporary service recovery.

## Output

- Execution results are stored in `outputs/latest_execution.json`.
- Application logs are stored in `outputs/resilience.log`.

## Limitations

- Uses local JSON demonstration data.
- Retry operations are simulated locally.
- The recovery mechanism does not provide distributed failover or persistent job recovery.

## Conclusion

The lab demonstrates operational resilience through structured logging, input validation, automatic retries, exception handling and recovery mechanisms. These techniques help maintain reliable agent execution when temporary failures or invalid inputs occur.