"""igprompts: Instagram Growth & Faceless Content Prompt Management Library."""

from __future__ import annotations

__version__ = "0.1.0"

from .core import get_prompt, list_prompts, render_pipeline, render_prompt
from .models import PromptDefinition

__all__ = [
    "__version__",
    "PromptDefinition",
    "get_prompt",
    "list_prompts",
    "render_pipeline",
    "render_prompt",
]
