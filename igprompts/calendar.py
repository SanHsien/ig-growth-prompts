"""Phase 4: Content Calendar Engine and Multi-Channel Exporters.

Converts workflow states, 7-day test ledgers, or topic lists into scheduled
calendar entries, and exports them into standard formats for:
- Notion Database (CSV)
- Airtable Content Calendar (CSV)
- Buffer / Social Schedulers (CSV)
- Markdown Visual Content Calendar
"""

from __future__ import annotations

import csv
import re
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from .core import md_cell
from .experiments import ExperimentRow, load_ledger
from .workflow import WorkflowState


@dataclass
class CalendarEntry:
    entry_id: str
    scheduled_date: str  # YYYY-MM-DD
    scheduled_time: str  # HH:MM
    channel: str         # "IG Reels", "IG Carousel", "Threads", "LinkedIn"
    title: str
    hook: str
    caption: str
    media_asset: str     # Path to SVG/video or description
    status: str = "Draft" # "Draft", "Ready", "Scheduled", "Published"
    target_metric: str = "views"
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def generate_calendar_from_ledger(
    ledger_rows: list[ExperimentRow],
    start_date: str | date,
    default_time: str = "18:00",
    default_channel: str = "IG Reels",
) -> list[CalendarEntry]:
    """Generate calendar entries from a 7-day experiment ledger."""
    if isinstance(start_date, str):
        curr_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    else:
        curr_date = start_date

    entries: list[CalendarEntry] = []
    for row in ledger_rows:
        if not (row.day.isascii() and row.day.isdecimal() and int(row.day) >= 1):
            raise ValueError(f"Ledger day '{row.day}' must be a positive whole number.")
        day_num = int(row.day)
        entry_date = curr_date + timedelta(days=day_num - 1)
        fmt = row.fields.get("format") or "Reels"
        channel = "IG Carousel" if "輪播" in fmt or "Carousel" in fmt else default_channel

        entries.append(
            CalendarEntry(
                entry_id=f"EXP-{row.day.zfill(2)}",
                scheduled_date=entry_date.strftime("%Y-%m-%d"),
                scheduled_time=default_time,
                channel=channel,
                title=row.fields.get("topic") or f"Day {row.day} 測試主題",
                hook=row.fields.get("hook") or "",
                caption=f"{row.fields.get('topic', '')}\n\n{row.fields.get('cta', '')}",
                media_asset=row.fields.get("format") or "未指定",
                status="Draft",
                target_metric=row.fields.get("primary_metric") or "views",
                notes=f"驗證假設: {row.fields.get('hypothesis', '')}",
            )
        )
    return entries


def generate_calendar_from_workflow_state(
    state: WorkflowState,
    start_date: str | date,
    default_time: str = "19:00",
) -> list[CalendarEntry]:
    """Generate a calendar entry from a completed workflow pipeline."""
    if isinstance(start_date, str):
        curr_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    else:
        curr_date = start_date

    cfg = state.config
    title = cfg.get("idea") or cfg.get("topic") or cfg.get("niche") or "未命名主題"
    channel = "IG Carousel" if state.series == "faceless_carousel" else "IG Reels"

    hook = ""
    # Extract hook if step 2 (faceless) or step 7 (reels) is completed
    s2 = state.steps.get(2) or state.steps.get(7)
    if s2 and s2.output:
        first_line = [ln for ln in s2.output.splitlines() if ln.strip() and not ln.startswith("【")]
        if first_line:
            hook = first_line[0]

    return [
        CalendarEntry(
            entry_id="WF-01",
            scheduled_date=curr_date.strftime("%Y-%m-%d"),
            scheduled_time=default_time,
            channel=channel,
            title=title,
            hook=hook,
            caption=cfg.get("content") or "",
            media_asset="slides/slide_01.svg" if channel == "IG Carousel" else "短影音腳本",
            status="Ready",
            target_metric="saves" if channel == "IG Carousel" else "views",
            notes=f"由 {state.series} 流水線產出",
        )
    ]


def generate_calendar_from_batch_dir(
    batch_dir: str | Path,
    start_date: str | date,
    default_time: str = "19:00",
    interval_days: int = 1,
) -> list[CalendarEntry]:
    """Scan all workflow_state.json files in batch output subdirectories and build a scheduled calendar."""
    p = Path(batch_dir)
    if not p.exists():
        raise FileNotFoundError(f"Batch directory not found: {p}")

    state_files = sorted(p.glob("*/workflow_state.json"))
    if not state_files:
        raise ValueError(f"No workflow_state.json found in {p}")

    if isinstance(start_date, str):
        curr_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    else:
        curr_date = start_date

    entries: list[CalendarEntry] = []
    for idx, sf in enumerate(state_files):
        entry_date = curr_date + timedelta(days=idx * interval_days)
        state = WorkflowState.load_checkpoint(sf)
        item_entries = generate_calendar_from_workflow_state(state, entry_date, default_time=default_time)
        for item in item_entries:
            item.entry_id = f"BATCH-{(idx + 1):02d}"
            entries.append(item)
    return entries



_NUMBER_RE = re.compile(r"[+-]?\d+(\.\d+)?")
_FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


def csv_safe(value: object, enabled: bool = True) -> str:
    """Neutralize spreadsheet formula injection (OWASP): prefix risky cells with a single quote.

    Plain numbers (including negatives) stay untouched so numeric columns keep working.
    """
    text = "" if value is None else str(value)
    if not enabled or not text.startswith(_FORMULA_PREFIXES) or _NUMBER_RE.fullmatch(text):
        return text
    return "'" + text


def _safe_row(row: dict[str, str], sanitize: bool) -> dict[str, str]:
    return {k: csv_safe(v, sanitize) for k, v in row.items()}


# ============================================================================
# Exporters (Notion, Airtable, Buffer, Markdown)
# ============================================================================

def export_notion_csv(
    entries: list[CalendarEntry], output_path: str | Path, *, sanitize: bool = True
) -> Path:
    """Export Notion Database compatible CSV (UTF-8 BOM)."""
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "ID",
        "Title",
        "Date",
        "Time",
        "Channel",
        "Status",
        "Hook",
        "Media Asset",
        "Target Metric",
        "Notes",
    ]
    with p.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for e in entries:
            writer.writerow(_safe_row({
                "ID": e.entry_id,
                "Title": e.title,
                "Date": e.scheduled_date,
                "Time": e.scheduled_time,
                "Channel": e.channel,
                "Status": e.status,
                "Hook": e.hook,
                "Media Asset": e.media_asset,
                "Target Metric": e.target_metric,
                "Notes": e.notes,
            }, sanitize))
    return p


def export_airtable_csv(
    entries: list[CalendarEntry], output_path: str | Path, *, sanitize: bool = True
) -> Path:
    """Export Airtable Content Calendar template compatible CSV (UTF-8 BOM)."""
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "Post Name",
        "Scheduled Date",
        "Platform",
        "Copy / Caption",
        "Hook",
        "Status",
        "Asset",
        "KPI",
    ]
    with p.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for e in entries:
            writer.writerow(_safe_row({
                "Post Name": e.title,
                "Scheduled Date": f"{e.scheduled_date}T{e.scheduled_time}:00",
                "Platform": e.channel,
                "Copy / Caption": e.caption,
                "Hook": e.hook,
                "Status": e.status,
                "Asset": e.media_asset,
                "KPI": e.target_metric,
            }, sanitize))
    return p


def export_buffer_csv(
    entries: list[CalendarEntry], output_path: str | Path, *, sanitize: bool = True
) -> Path:
    """Export Buffer social scheduler compatible CSV."""
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["Date", "Time", "Text", "Media", "Channel"]
    with p.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for e in entries:
            text = f"{e.hook}\n\n{e.title}\n\n{e.caption}".strip()
            writer.writerow(_safe_row({
                "Date": e.scheduled_date,
                "Time": e.scheduled_time,
                "Text": text,
                "Media": e.media_asset,
                "Channel": e.channel,
            }, sanitize))
    return p


def export_markdown_calendar(entries: list[CalendarEntry], output_path: str | Path | None = None) -> str:
    """Export readable Markdown Content Calendar table."""
    lines = [
        "# 內容發布日曆 (Content Calendar)",
        "",
        f"- 排定篇數：{len(entries)} 篇",
        f"- 日期區間：{entries[0].scheduled_date if entries else 'N/A'} ~ {entries[-1].scheduled_date if entries else 'N/A'}",
        "",
        "| ID | 發布日期 | 時間 | 渠道 | 主題／標題 | 開場鉤子 | 狀態 | KPI |",
        "|:---|:---|:---|:---|:---|:---|:---|:---|",
    ]
    for e in entries:
        hook_display = e.hook[:20] + "..." if len(e.hook) > 20 else (e.hook or "—")
        lines.append(
            f"| `{md_cell(e.entry_id)}` | {md_cell(e.scheduled_date)} | {md_cell(e.scheduled_time)} | "
            f"{md_cell(e.channel)} | {md_cell(e.title)} | {md_cell(hook_display)} | "
            f"`{md_cell(e.status)}` | `{md_cell(e.target_metric)}` |"
        )
    lines.append("")

    doc = "\n".join(lines)
    if output_path:
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(doc, encoding="utf-8")
    return doc
