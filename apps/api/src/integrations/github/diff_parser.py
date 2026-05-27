from __future__ import annotations

from pathlib import PurePosixPath

from unidiff import PatchSet

from src.agent.state import FileDiff

LANG_BY_EXT = {
    ".py": "python",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".java": "java",
    ".kt": "kotlin",
    ".sql": "sql",
    ".md": "markdown",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
}


def _detect_lang(path: str) -> str | None:
    return LANG_BY_EXT.get(PurePosixPath(path).suffix.lower())


def parse_unified_diff(diff_text: str) -> list[FileDiff]:
    patch = PatchSet(diff_text)
    out: list[FileDiff] = []
    for f in patch:
        path = f.target_file.removeprefix("b/") if f.target_file != "/dev/null" else f.source_file.removeprefix("a/")
        out.append(
            {
                "path": path,
                "patch": str(f),
                "added": f.added,
                "removed": f.removed,
                "language": _detect_lang(path),
            }
        )
    return out
