from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_graph_compiles() -> None:
    from src.agent.graph import build_graph

    g = build_graph()
    assert g is not None


@pytest.mark.asyncio
async def test_match_patterns_clusters() -> None:
    from src.agent.nodes.match_patterns import match_patterns

    state = {
        "repo_full_name": "x/y",
        "pr_number": 1,
        "head_sha": "abc",
        "diff": None,
        "files": [],
        "memory_hits": [
            {"id": "1", "score": 0.9, "payload": {"pattern_label": "p1", "description": "d"}},
            {"id": "2", "score": 0.85, "payload": {"pattern_label": "p1", "description": "d"}},
            {"id": "3", "score": 0.5, "payload": {"pattern_label": "p2", "description": "d"}},
        ],
        "patterns": [],
        "feedback": [],
        "published": False,
        "errors": [],
    }
    out = await match_patterns(state)
    assert any(p["name"] == "p1" for p in out["patterns"])
    assert all(p["name"] != "p2" for p in out["patterns"])
