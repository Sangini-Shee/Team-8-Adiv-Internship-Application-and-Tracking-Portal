from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def test_langchain_create_agent_is_implemented():
    s = (ROOT / "integrations/langchain_agent.py").read_text(encoding="utf-8")
    assert "from langchain.agents import create_agent" in s and "create_agent(" in s

def test_langgraph_stategraph_is_implemented():
    s = (ROOT / "integrations/langgraph_orchestrator.py").read_text(encoding="utf-8")
    assert "from langgraph.graph import StateGraph" in s
    assert "StateGraph(" in s and "add_conditional_edges" in s

def test_mcp_server_and_client_are_implemented():
    server = (ROOT / "mcp_server.py").read_text(encoding="utf-8")
    client = (ROOT / "integrations/mcp_client.py").read_text(encoding="utf-8")
    assert "@mcp.tool()" in server
    assert "ClientSession" in client and "call_tool" in client

def test_swarms_sequential_workflow_is_implemented():
    s = (ROOT / "integrations/swarms_workflow.py").read_text(encoding="utf-8")
    assert "from swarms import Agent, SequentialWorkflow" in s
    assert "SequentialWorkflow(" in s
