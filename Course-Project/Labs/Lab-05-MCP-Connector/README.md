# Lab 05 – MCP Connector

## 1. Overview
This lab demonstrates the implementation of the Model Context Protocol (MCP) to connect an AI application with external tools through a standardized client-server architecture.

The MCP server exposes internship portal functionalities, while the MCP client discovers and invokes the available tools.

## 2. Objectives
- Understand the Model Context Protocol.
- Implement an MCP server using FastMCP.
- Develop an MCP client using ClientSession.
- Register and discover tools.
- Invoke external tools through MCP.
- Integrate the existing Internship Portal data.

## 3. Technologies Used
- Python 3.12
- MCP SDK 1.26.0
- FastMCP
- Asyncio
- Pytest

## 4. Project Structure
```text
Lab-05-MCP-Connector/
├── server/
│   ├── __init__.py
│   └── mcp_server.py
├── client/
│   ├── __init__.py
│   └── mcp_client.py
├── tests/
│   └── test_mcp_tools.py
├── outputs/
├── main.py
├── requirements.txt
└── README.md
```

## 5. Architecture

The implementation follows this workflow:

1. The MCP client starts the MCP server using standard input/output transport.
2. The client establishes a connection and initializes the session.
3. The client discovers tools registered by the server.
4. The user selects an operation.
5. The client invokes the corresponding MCP tool.
6. The server retrieves information from the Internship Portal JSON datasets.
7. The result is returned to the client.

## 6. Implemented MCP Tools

### 1. get_student_profile
Retrieves a student profile using the student ID.

### 2. list_internships
Returns the available internship opportunities.

### 3. get_internship_details
Retrieves detailed information about an internship using its ID.

## 7. Execution

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the MCP application:

```bash
python main.py
```

Select an operation from the displayed menu and provide the requested ID.

## 8. Testing

Execute the automated test suite:

```bash
python -m pytest -v
```

**Result:** All 4 automated tests passed.

Tests cover:
- MCP server tool discovery
- Student profile retrieval
- Internship listing
- Internship detail retrieval

## 9. Outcome
Successfully implemented an MCP client-server application that exposes Internship Portal functionalities as discoverable and callable tools.

## 10. Limitations
The current implementation uses local JSON datasets and standard input/output transport. It is a demonstration implementation and does not provide production authentication or remote deployment.
