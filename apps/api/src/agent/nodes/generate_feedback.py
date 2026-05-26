"""Generate structured review feedback using Gemini.

The node takes the parsed diff, recalled memory hits, and matched patterns,
asks Gemini for a JSON list of comments conforming to a strict schema, and
sanitizes/clamps the output before handing it to the publish step.
"""

from __future__ import annotations

import json
from typing import Any

from src.agent.state import FeedbackComment, ReviewState
from src.llm.gemini import GeminiConfigError, get_gemini_client
from src.observability.logging import get_logger

log = get_logger(__name__)

MAX_FILES_IN_PROMPT = 25
MAX_PATCH_CHARS = 4000
MAX_COMMENTS = 50

SYSTEM_INSTRUCTION = (
    "You are Lineage, a senior code reviewer. Produce concise, actionable, "
    "line-anchored review comments grounded in the supplied diff. Cite the "
    "matched patterns when relevant. Do not invent file paths or line numbers."
)

RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "comments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "line": {"type": "integer", "minimum": 1},
                    "side": {"type": "string", "enum": ["LEFT", "RIGHT"]},
                    "severity": {"type": "string", "enum": ["info", "warn", "block"]},
                    "body": {"type": "string"},
                },
                "required": ["path", "line", "side", "severity", "body"],
            },
        }
    },
    "required": ["comments"],
}


def _truncate(patch: str) -> str:
    return patch if len(patch) <= MAX_PATCH_CHARS else patch[:MAX_PATCH_CHARS] + "\n...[truncated]"


def _build_prompt(state: ReviewState) -> str:
    files = state["files"][:MAX_FILES_IN_PROMPT]
    diff_block = "\n\n".join(
        f"### {f['path']} (+{f['added']}/-{f['removed']})\n```\n{_truncate(f['patch'])}\n```"
        for f in files
    )
    patterns_block = json.dumps(
        [
            {"name": p["name"], "description": p["description"], "confidence": round(p["confidence"], 3)}
            for p in state["patterns"]
        ],
        indent=2,
    )
    return (
        f"Repository: {state['repo_full_name']}\n"
        f"Pull request: #{state['pr_number']}\n\n"
        f"Matched patterns (from prior review memory):\n{patterns_block}\n\n"
        f"Diff:\n{diff_block}\n\n"
        "Return JSON matching the schema. Only comment on issues you can pin "
        "to a specific changed line in the diff."
    )


def _sanitize_comments(payload: Any, valid_paths: set[str]) -> list[FeedbackComment]:
    if not isinstance(payload, dict):
        return []
    raw = payload.get("comments") or []
    out: list[FeedbackComment] = []
    for entry in raw[:MAX_COMMENTS]:
        if not isinstance(entry, dict):
            continue
        path = entry.get("path")
        line = entry.get("line")
        body = entry.get("body")
        if not (isinstance(path, str) and isinstance(line, int) and isinstance(body, str)):
            continue
        if path not in valid_paths:
            continue
        out.append(
            {
                "path": path,
                "line": int(line),
                "side": entry.get("side", "RIGHT") if entry.get("side") in {"LEFT", "RIGHT"} else "RIGHT",
                "body": body.strip(),
                "severity": entry.get("severity", "info")
                if entry.get("severity") in {"info", "warn", "block"}
                else "info",
            }
        )
    return out


async def generate_feedback(state: ReviewState) -> ReviewState:
    if not state["files"]:
        log.info("agent.generate_feedback.skip", reason="no_files")
        return {**state, "feedback": []}

    try:
        client = get_gemini_client()
    except GeminiConfigError as e:
        log.warning("agent.generate_feedback.no_llm", reason=str(e))
        return {**state, "feedback": [], "errors": [*state["errors"], str(e)]}

    prompt = _build_prompt(state)
    payload = await client.generate_json(
        prompt,
        schema=RESPONSE_SCHEMA,
        system_instruction=SYSTEM_INSTRUCTION,
    )
    feedback = _sanitize_comments(payload, valid_paths={f["path"] for f in state["files"]})
    log.info("agent.generate_feedback", count=len(feedback))
    return {**state, "feedback": feedback}
