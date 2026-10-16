"""Prompt lookup and rendering. Tool-agnostic: output is plain text for any AI tool."""

from __future__ import annotations

from typing import Any

from .models import FACELESS_CAROUSEL_PROMPTS, PROMPTS, SHORT_VIDEO_REELS_PROMPTS, PromptDefinition

SERIES_FACELESS = "faceless_carousel"
SERIES_REELS = "short_video_reels"
SERIES_TITLES = {
    SERIES_FACELESS: "圖文與不露臉精準留存體系",
    SERIES_REELS: "短影音爆款與假設驗證體系",
}
_SERIES_ALIASES = {
    SERIES_FACELESS: SERIES_FACELESS,
    "faceless": SERIES_FACELESS,
    "carousel": SERIES_FACELESS,
    "claude_ig": SERIES_FACELESS,  # legacy name from v0.2 state files
    SERIES_REELS: SERIES_REELS,
    "reels": SERIES_REELS,
    "chatgpt_reels": SERIES_REELS,  # legacy name
}


def normalize_series(series: str) -> str:
    key = (series or "").strip().lower()
    if key not in _SERIES_ALIASES:
        raise ValueError(f"Unknown series '{series}'. Use one of: {SERIES_FACELESS}, {SERIES_REELS}.")
    return _SERIES_ALIASES[key]


def list_prompts(series: str | None = None) -> list[PromptDefinition]:
    """All prompts sorted by ID, or only one series."""
    if series is None:
        source = PROMPTS
    elif normalize_series(series) == SERIES_FACELESS:
        source = FACELESS_CAROUSEL_PROMPTS
    else:
        source = SHORT_VIDEO_REELS_PROMPTS
    return [source[i] for i in sorted(source)]


def get_prompt(identifier: int | str) -> PromptDefinition:
    """Look up a prompt by ID (1-12, "06" also works) or by key."""
    if isinstance(identifier, int) and identifier in PROMPTS:
        return PROMPTS[identifier]
    if isinstance(identifier, str):
        cleaned = identifier.strip()
        if cleaned.isdigit() and int(cleaned) in PROMPTS:
            return PROMPTS[int(cleaned)]
        for p in PROMPTS.values():
            if p.key == cleaned:
                return p
    valid = ", ".join(f"{p.id:02d} ({p.key})" for p in PROMPTS.values())
    raise KeyError(f"Invalid prompt identifier '{identifier}'. Available: [{valid}].")


def render_prompt(
    identifier: int | str,
    variables: dict[str, Any] | None = None,
    *,
    fallback_placeholder: bool = False,
) -> str:
    """Fill a template. Missing variables raise, or become ``<name>`` when allowed."""
    definition = get_prompt(identifier)
    vars_map = variables or {}
    formatted: dict[str, str] = {}
    missing: list[str] = []

    for var in definition.variables:
        val = vars_map.get(var)
        if val is None or str(val).strip() == "":
            if fallback_placeholder:
                formatted[var] = f"<{var}>"
            else:
                missing.append(var)
        else:
            formatted[var] = str(val).strip()

    if missing:
        raise ValueError(
            f"Prompt {definition.id:02d} ({definition.title}) is missing required variables: "
            f"{', '.join(missing)}"
        )
    return definition.template.format(**formatted)


def render_pipeline(config: dict[str, Any], series: str = SERIES_FACELESS) -> str:
    """One Markdown document with every prompt of a series, ready to paste anywhere."""
    series = normalize_series(series)
    lines: list[str] = [
        f"# Content Pipeline: {SERIES_TITLES[series]}",
        "",
        "> 純文字提示詞，可貼進任何 AI 工具（聊天介面、CLI、API、自建 Agent）。",
        "",
    ]
    for p in list_prompts(series):
        lines.append(f"## Prompt {p.id:02d}（第 {p.series_index} 步）: {p.title}")
        lines.append(f"- Key: `{p.key}` | Role: {p.role}")
        lines.append("")
        lines.append("```text")
        lines.append(render_prompt(p.id, config, fallback_placeholder=True))
        lines.append("```")
        lines.append("")
    return "\n".join(lines)
