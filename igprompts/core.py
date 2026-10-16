"""Core logic for rendering and validating prompt templates."""

from __future__ import annotations

from typing import Any

from .models import PROMPTS, PromptDefinition


def list_prompts() -> list[PromptDefinition]:
    """Return all available prompts sorted by ID."""
    return [PROMPTS[i] for i in sorted(PROMPTS.keys())]


def get_prompt(prompt_id: int) -> PromptDefinition:
    """Retrieve a prompt definition by its numerical ID (1-5)."""
    if prompt_id not in PROMPTS:
        valid_ids = ", ".join(str(i) for i in sorted(PROMPTS.keys()))
        raise KeyError(f"Invalid prompt ID {prompt_id}. Expected one of [{valid_ids}].")
    return PROMPTS[prompt_id]


def render_prompt(
    prompt_id: int,
    variables: dict[str, Any] | None = None,
    *,
    fallback_placeholder: bool = False,
) -> str:
    """Render a prompt template with provided variables.

    If fallback_placeholder is True, missing variables will retain their `{var_name}`
    markers for manual editing later.
    """
    definition = get_prompt(prompt_id)
    vars_map = variables or {}

    formatted_vars: dict[str, str] = {}
    missing: list[str] = []

    for var in definition.variables:
        val = vars_map.get(var)
        if val is None or str(val).strip() == "":
            if fallback_placeholder:
                formatted_vars[var] = f"<{var}>"
            else:
                missing.append(var)
        else:
            formatted_vars[var] = str(val).strip()

    if missing:
        raise ValueError(
            f"Prompt {prompt_id} ({definition.title}) is missing required variables: "
            f"{', '.join(missing)}"
        )

    return definition.template.format(**formatted_vars)


def render_pipeline(config: dict[str, Any]) -> str:
    """Generate a combined markdown document for the 5-step end-to-end pipeline."""
    lines: list[str] = [
        "# End-to-End Content Generation Pipeline",
        "",
        "> This document contains the full sequence of 5 prompts tailored with your project parameters.",
        "",
    ]

    for p in list_prompts():
        lines.append(f"## Step {p.id}: {p.title}")
        lines.append("")
        rendered = render_prompt(p.id, config, fallback_placeholder=True)
        lines.append("```text")
        lines.append(rendered)
        lines.append("```")
        lines.append("")

    return "\n".join(lines)
