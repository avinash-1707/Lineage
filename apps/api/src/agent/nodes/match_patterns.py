from __future__ import annotations

from collections import defaultdict

from src.agent.state import Pattern, ReviewState
from src.observability.logging import get_logger

log = get_logger(__name__)

MIN_CLUSTER = 2
MIN_AVG_SCORE = 0.72


async def match_patterns(state: ReviewState) -> ReviewState:
    clusters: dict[str, list[dict]] = defaultdict(list)
    for hit in state["memory_hits"]:
        label = hit["payload"].get("pattern_label") or "uncategorized"
        clusters[label].append(hit)

    patterns: list[Pattern] = []
    for label, hits in clusters.items():
        if label == "uncategorized" or len(hits) < MIN_CLUSTER:
            continue
        avg = sum(h["score"] for h in hits) / len(hits)
        if avg < MIN_AVG_SCORE:
            continue
        patterns.append(
            {
                "name": label,
                "description": hits[0]["payload"].get("description", ""),
                "confidence": avg,
                "source_ids": [h["id"] for h in hits],
            }
        )

    log.info("agent.match_patterns", patterns=len(patterns))
    return {**state, "patterns": patterns}
