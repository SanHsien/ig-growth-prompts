"""igprompts: tool-agnostic Instagram content prompt library and workflow."""

from __future__ import annotations

__version__ = "0.3.0"

from .core import (
    SERIES_FACELESS,
    SERIES_REELS,
    get_prompt,
    list_prompts,
    normalize_series,
    render_pipeline,
    render_prompt,
)
from .experiments import build_report, load_ledger, write_plan
from .models import PromptDefinition
from .providers import (
    CallableProvider,
    CommandProvider,
    DryRunProvider,
    ManualProvider,
    WorkflowProvider,
)
from .renderer import (
    SlideData,
    SlideSpecError,
    parse_slide_spec,
    render_slides,
    render_slides_from_answer,
    render_svg_card,
)
from .workflow import StepRecord, WorkflowRunner, WorkflowState

__all__ = [
    "__version__",
    "SERIES_FACELESS",
    "SERIES_REELS",
    "CallableProvider",
    "CommandProvider",
    "DryRunProvider",
    "ManualProvider",
    "PromptDefinition",
    "SlideData",
    "SlideSpecError",
    "StepRecord",
    "WorkflowProvider",
    "WorkflowRunner",
    "WorkflowState",
    "build_report",
    "get_prompt",
    "list_prompts",
    "load_ledger",
    "normalize_series",
    "parse_slide_spec",
    "render_pipeline",
    "render_prompt",
    "render_slides",
    "render_slides_from_answer",
    "render_svg_card",
    "write_plan",
]
