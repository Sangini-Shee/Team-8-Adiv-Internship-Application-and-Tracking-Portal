"""LangGraph orchestration for the student-facing portal assistant."""
import os
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from assistant_service import _local_answer

class PortalAssistantState(TypedDict, total=False):
    question: str
    student_id: str
    mcp_context: str
    answer: str
    engine: str
    swarm_review: str
    error: str

def _mcp_context_node(state: PortalAssistantState) -> dict:
    try:
        from integrations.mcp_client import call_mcp_tool
        result = call_mcp_tool("get_student_profile", {"student_id": state["student_id"]})
        return {"mcp_context": result, "engine": "MCP + LangGraph"}
    except Exception as exc:
        return {"mcp_context": "", "error": f"MCP unavailable: {exc}", "engine": "Local fallback"}

def _route_after_mcp(state: PortalAssistantState) -> str:
    return "langchain" if (os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY")) else "local"

def _langchain_node(state: PortalAssistantState) -> dict:
    try:
        from integrations.langchain_agent import ask_langchain
        prompt = (
            f"Signed-in student ID: {state['student_id']}. "
            f"Profile context retrieved through MCP: {state.get('mcp_context', '')}. "
            f"Answer using portal tools. Question: {state['question']}"
        )
        return {"answer": ask_langchain(prompt), "engine": "LangChain + LangGraph"}
    except Exception as exc:
        return {"error": f"LangChain unavailable: {exc}", "answer": "", "engine": "Local fallback"}

def _route_after_langchain(state: PortalAssistantState) -> str:
    has_provider = any(os.getenv(k) for k in ("OPENAI_API_KEY", "GOOGLE_API_KEY", "ANTHROPIC_API_KEY"))
    return "swarms" if state.get("answer") and has_provider else "local"

def _swarms_node(state: PortalAssistantState) -> dict:
    try:
        from integrations.swarms_workflow import run_swarms_workflow
        task = (
            "Review this internship portal answer for factual grounding, clarity and policy safety. "
            "Do not invent facts or approve applications.\n"
            f"Student question: {state['question']}\nDraft answer: {state['answer']}\n"
            f"MCP profile context: {state.get('mcp_context', '')}"
        )
        reviewed = run_swarms_workflow(task)
        return {"swarm_review": str(reviewed), "engine": "LangGraph + LangChain + Swarms + MCP"}
    except Exception as exc:
        return {"error": f"Swarms review unavailable: {exc}"}

def _local_node(state: PortalAssistantState) -> dict:
    return {"answer": _local_answer(state["question"], state["student_id"]),
            "engine": "LangGraph + MCP + local fallback"}

def build_portal_assistant_graph():
    graph = StateGraph(PortalAssistantState)
    graph.add_node("mcp_context", _mcp_context_node)
    graph.add_node("langchain_agent", _langchain_node)
    graph.add_node("swarms_review", _swarms_node)
    graph.add_node("local_fallback", _local_node)
    graph.add_edge(START, "mcp_context")
    graph.add_conditional_edges("mcp_context", _route_after_mcp,
                                {"langchain": "langchain_agent", "local": "local_fallback"})
    graph.add_conditional_edges("langchain_agent", _route_after_langchain,
                                {"swarms": "swarms_review", "local": "local_fallback"})
    graph.add_edge("swarms_review", END)
    graph.add_edge("local_fallback", END)
    return graph.compile()

def run_portal_assistant(question: str, student_id: str) -> dict:
    result = build_portal_assistant_graph().invoke(
        {"question": question, "student_id": student_id}
    )
    answer = result.get("swarm_review") or result.get("answer") or (
        "I couldn't complete that request. Please try again or contact the coordinator."
    )
    return {"answer": answer, "engine": result.get("engine", "LangGraph"),
            "internal_error": result.get("error", "")}
