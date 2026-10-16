"""igprompts: Instagram Growth & Faceless Content Prompt Management Library."""

from __future__ import annotations

__version__ = "0.2.0"

from .core import get_prompt, list_prompts, render_pipeline, render_prompt
from .models import PromptDefinition
from .renderer import SlideData, generate_carousel_from_workflow, render_svg_card
from .workflow import (
    CallableProvider,
    DryRunProvider,
    StepRecord,
    WorkflowProvider,
    WorkflowRunner,
    WorkflowState,
)

__all__ = [
    "__version__",
    "CallableProvider",
    "DryRunProvider",
    "PromptDefinition",
    "SlideData",
    "StepRecord",
    "WorkflowProvider",
    "WorkflowRunner",
    "WorkflowState",
    "generate_carousel_from_workflow",
    "get_prompt",
    "list_prompts",
    "render_pipeline",
    "render_prompt",
    "render_svg_card",
]
