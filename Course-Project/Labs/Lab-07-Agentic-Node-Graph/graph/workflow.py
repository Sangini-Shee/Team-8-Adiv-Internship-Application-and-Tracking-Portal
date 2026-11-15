
from langgraph.graph import StateGraph, START, END

from graph.state import InternshipState
from graph.nodes import (
    retrieve_student,
    retrieve_opportunities,
    recommend_opportunities,
    finalize
)


def check_student(state):
    if state.get("error") or not state.get("student"):
        return "finish"
    return "retrieve_opportunities"


def check_opportunities(state):
    if state.get("error") or not state.get("opportunities"):
        return "finish"
    return "recommend"


def build_workflow():
    builder = StateGraph(InternshipState)

    builder.add_node("retrieve_student", retrieve_student)
    builder.add_node("retrieve_opportunities", retrieve_opportunities)
    builder.add_node("recommend", recommend_opportunities)
    builder.add_node("finish", finalize)

    builder.add_edge(START, "retrieve_student")

    builder.add_conditional_edges(
        "retrieve_student",
        check_student,
        {
            "retrieve_opportunities": "retrieve_opportunities",
            "finish": "finish"
        }
    )

    builder.add_conditional_edges(
        "retrieve_opportunities",
        check_opportunities,
        {
            "recommend": "recommend",
            "finish": "finish"
        }
    )

    builder.add_edge("recommend", "finish")
    builder.add_edge("finish", END)

    return builder.compile()


internship_graph = build_workflow()
