from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from src.agent.nodes.generate_feedback import generate_feedback
from src.agent.nodes.match_patterns import match_patterns
from src.agent.nodes.parse_diff import parse_diff
from src.agent.nodes.publish_review import publish_review
from src.agent.nodes.retrieve_memory import retrieve_memory
from src.agent.state import ReviewState


def build_graph():
    g: StateGraph = StateGraph(ReviewState)

    g.add_node("parse_diff", parse_diff)
    g.add_node("retrieve_memory", retrieve_memory)
    g.add_node("match_patterns", match_patterns)
    g.add_node("generate_feedback", generate_feedback)
    g.add_node("publish_review", publish_review)

    g.add_edge(START, "parse_diff")
    g.add_edge("parse_diff", "retrieve_memory")
    g.add_edge("retrieve_memory", "match_patterns")
    g.add_edge("match_patterns", "generate_feedback")
    g.add_conditional_edges(
        "generate_feedback",
        lambda s: "publish" if s.get("feedback") else "skip",
        {"publish": "publish_review", "skip": END},
    )
    g.add_edge("publish_review", END)

    return g.compile()
