"""Batch Queue Processor for handling multiple topics sequentially."""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .calendar import CalendarEntry
from .core import normalize_series
from .providers import DryRunProvider, ManualProvider, WorkflowProvider
from .workflow import WorkflowRunner, WorkflowState


_UNSAFE_ID_RE = re.compile(r'[\/:*?"<>|\x00-\x1f]')


def _validate_ids(items: list[TopicItem]) -> None:
    """Item ids become directory names: reject path-unsafe and duplicate ids."""
    seen: set[str] = set()
    for item in items:
        bad = (
            not item.id
            or _UNSAFE_ID_RE.search(item.id)
            or item.id.startswith(".")
            or item.id != item.id.strip()
            or item.id.endswith(".")
        )
        if bad:
            raise ValueError(f"Topic id {item.id!r} is not usable as a directory name.")
        if item.id in seen:
            raise ValueError(f"Duplicate topic id {item.id!r}: ids must be unique.")
        seen.add(item.id)


@dataclass
class TopicItem:
    id: str
    topic: str
    niche: str = ""
    audience: str = ""
    series: str = "faceless_carousel"
    extra: dict[str, Any] | None = None


def load_topic_queue(file_path: str | Path) -> list[TopicItem]:
    """Load topic items from a JSON or CSV queue file."""
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"Topic queue file not found: {p}")

    items: list[TopicItem] = []
    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text(encoding="utf-8-sig"))
        if not isinstance(data, list):
            raise ValueError("JSON topic queue must be an array of objects.")
        for idx, obj in enumerate(data, start=1):
            items.append(
                TopicItem(
                    id=str(obj.get("id") or f"T{idx:02d}"),
                    topic=str(obj.get("topic") or obj.get("idea") or ""),
                    niche=str(obj.get("niche") or ""),
                    audience=str(obj.get("audience") or ""),
                    series=normalize_series(obj.get("series") or "faceless_carousel"),
                    extra=obj,
                )
            )
    elif p.suffix.lower() == ".csv":
        with p.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, start=1):
                items.append(
                    TopicItem(
                        id=row.get("id") or f"T{idx:02d}",
                        topic=row.get("topic") or row.get("idea") or "",
                        niche=row.get("niche") or "",
                        audience=row.get("audience") or "",
                        series=normalize_series(row.get("series") or "faceless_carousel"),
                        extra=dict(row),
                    )
                )
    else:
        raise ValueError("Unsupported topic queue format. Please use .json or .csv.")

    if not items:
        raise ValueError("Topic queue is empty.")
    _validate_ids(items)
    return items


def run_batch_queue(
    items: list[TopicItem],
    output_dir: str | Path,
    provider: WorkflowProvider | None = None,
) -> list[dict[str, Any]]:
    """Execute each topic in the queue through its respective series runner."""
    _validate_ids(items)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []

    for item in items:
        item_dir = out / f"{item.id}_{item.series}"
        config: dict[str, Any] = {
            "niche": item.niche,
            "audience": item.audience,
            "topic": item.topic,
            "idea": item.topic,
        }
        if item.extra:
            config.update(item.extra)

        item_provider: WorkflowProvider = provider or DryRunProvider()
        if isinstance(item_provider, ManualProvider):
            # One handoff folder per topic, or topics overwrite each other's prompts and reuse each other's answers.
            item_provider = ManualProvider(item_provider.handoff_dir / item_dir.name)

        runner = WorkflowRunner(
            config=config,
            series=item.series,
            provider=item_provider,
        )
        runner.run_all(checkpoint_path=item_dir / "workflow_state.json")
        artifacts = runner.export_manifest(item_dir)

        results.append({
            "id": item.id,
            "topic": item.topic,
            "series": item.series,
            "dir": str(item_dir),
            "manifest": str(artifacts["manifest"]),
        })

    return results
