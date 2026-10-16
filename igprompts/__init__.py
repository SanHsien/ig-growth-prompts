"""igprompts: tool-agnostic Instagram content prompt library and workflow."""

from __future__ import annotations

__version__ = "0.4.0"

from .batch import TopicItem, load_topic_queue, run_batch_queue
from .calendar import (
    CalendarEntry,
    export_airtable_csv,
    export_buffer_csv,
    export_markdown_calendar,
    export_notion_csv,
    generate_calendar_from_ledger,
    generate_calendar_from_workflow_state,
)
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
    "CalendarEntry",
    "CallableProvider",
    "CommandProvider",
    "DryRunProvider",
    "ManualProvider",
    "PromptDefinition",
    "SlideData",
    "SlideSpecError",
    "StepRecord",
    "TopicItem",
    "WorkflowProvider",
    "WorkflowRunner",
    "WorkflowState",
    "build_report",
    "export_airtable_csv",
    "export_buffer_csv",
    "export_markdown_calendar",
    "export_notion_csv",
    "generate_calendar_from_ledger",
    "generate_calendar_from_workflow_state",
    "get_prompt",
    "list_prompts",
    "load_ledger",
    "load_topic_queue",
    "normalize_series",
    "parse_slide_spec",
    "render_pipeline",
    "render_prompt",
    "render_slides",
    "render_slides_from_answer",
    "render_svg_card",
    "run_batch_queue",
    "write_plan",
]
