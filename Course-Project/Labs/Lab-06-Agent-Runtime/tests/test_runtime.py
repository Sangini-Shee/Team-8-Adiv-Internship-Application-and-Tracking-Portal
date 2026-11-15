
import pytest

from runtime.agent_runtime import AgentRuntime
from runtime.tool_manager import ToolManager


def sample_lookup(student_id):
    students = {
        "STU001": {
            "name": "Sangini Shee",
            "department": "CS-AI",
            "cgpa": 8.4
        }
    }
    return students.get(student_id, {"error": "Student not found"})


def test_tool_registration():
    runtime = AgentRuntime()

    runtime.register_tool(
        "student_lookup",
        sample_lookup,
        "Retrieve student profile"
    )

    tools = runtime.get_available_tools()

    assert len(tools) == 1
    assert tools[0]["name"] == "student_lookup"


def test_successful_agent_execution():
    runtime = AgentRuntime()

    runtime.register_tool(
        "student_lookup",
        sample_lookup,
        "Retrieve student profile"
    )

    result = runtime.run(
        "Retrieve student information",
        "student_lookup",
        {"student_id": "STU001"}
    )

    assert result["status"] == "success"
    assert result["result"]["name"] == "Sangini Shee"


def test_execution_history():
    runtime = AgentRuntime()

    runtime.register_tool(
        "student_lookup",
        sample_lookup,
        "Retrieve student profile"
    )

    runtime.run(
        "Find student",
        "student_lookup",
        {"student_id": "STU001"}
    )

    history = runtime.get_execution_history()

    assert len(history) == 1
    assert history[0]["status"] == "success"
    assert history[0]["tool"] == "student_lookup"


def test_invalid_tool():
    runtime = AgentRuntime()

    result = runtime.run(
        "Find student",
        "unknown_tool",
        {}
    )

    assert result["status"] == "failed"
    assert "not registered" in result["error"]


def test_empty_task():
    runtime = AgentRuntime()

    result = runtime.run(
        "",
        "student_lookup",
        {"student_id": "STU001"}
    )

    assert result["status"] == "failed"
    assert "Task description" in result["error"]


def test_execution_limit():
    runtime = AgentRuntime(max_steps=2)

    runtime.register_tool(
        "student_lookup",
        sample_lookup,
        "Retrieve student profile"
    )

    first = runtime.run(
        "Find student",
        "student_lookup",
        {"student_id": "STU001"}
    )

    second = runtime.run(
        "Find student",
        "student_lookup",
        {"student_id": "STU001"}
    )

    third = runtime.run(
        "Find student",
        "student_lookup",
        {"student_id": "STU001"}
    )

    assert first["status"] == "success"
    assert second["status"] == "success"
    assert third["status"] == "limit_reached"


def test_invalid_tool_registration():
    manager = ToolManager()

    with pytest.raises(ValueError):
        manager.register_tool(
            "",
            sample_lookup,
            "Invalid tool"
        )
