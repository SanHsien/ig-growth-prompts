"""Workflow state machine and runner.

Step lifecycle: pending -> running -> completed | awaiting_response | failed.
``awaiting_response`` means the provider has no answer yet (manual handoff);
the run stops there and ``--resume`` continues once the answer exists.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from .core import get_prompt, list_prompts, normalize_series, render_prompt
from .providers import DryRunProvider, WorkflowProvider

STATE_FILE = "workflow_state.json"
MANIFEST_FILE = "pipeline_manifest.md"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class StepRecord:
    step_id: int
    key: str
    title: str
    series_index: int
    prompt_rendered: str = ""
    output: str = ""
    status: str = "pending"
    started_at: str | None = None
    completed_at: str | None = None
    error: str | None = None


@dataclass
class WorkflowState:
    series: str = "faceless_carousel"
    config: dict[str, Any] = field(default_factory=dict)
    steps: dict[int, StepRecord] = field(default_factory=dict)
    provider: str = "dry-run"
    created_at: str = field(default_factory=_utc_now_iso)
    updated_at: str = field(default_factory=_utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "series": self.series,
            "provider": self.provider,
            "config": self.config,
            "steps": {str(k): asdict(v) for k, v in self.steps.items()},
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkflowState:
        state = cls(
            series=normalize_series(data.get("series", "faceless_carousel")),
            config=data.get("config", {}),
            provider=data.get("provider", "dry-run"),
            created_at=data.get("created_at", _utc_now_iso()),
            updated_at=data.get("updated_at", _utc_now_iso()),
        )
        for k, v in data.get("steps", {}).items():
            state.steps[int(k)] = StepRecord(**v)
        return state

    def save_checkpoint(self, path: str | Path) -> None:
        self.updated_at = _utc_now_iso()
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = None
        try:
            with NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=p.parent,
                prefix=f".{p.name}.", suffix=".tmp", delete=False,
            ) as temporary:
                temporary_path = Path(temporary.name)
                json.dump(self.to_dict(), temporary, ensure_ascii=False, indent=2)
                temporary.flush()
                os.fsync(temporary.fileno())
            # Close the temporary file before replacement, including on Windows.
            temporary_path.replace(p)
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)

    @classmethod
    def load_checkpoint(cls, path: str | Path) -> WorkflowState:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Checkpoint file not found: {p}")
        return cls.from_dict(json.loads(p.read_text(encoding="utf-8")))

    def step_output(self, step_id: int) -> str:
        rec = self.steps.get(step_id)
        return rec.output if rec and rec.status == "completed" else ""


class WorkflowRunner:
    """Run one series step by step and persist state after every step."""

    def __init__(
        self,
        config: dict[str, Any],
        series: str = "faceless_carousel",
        provider: WorkflowProvider | None = None,
        state: WorkflowState | None = None,
        prompt_addenda: dict[int, str] | None = None,
    ):
        self.series = normalize_series(state.series if state else series)
        self.config = dict(config)
        self.provider = provider or DryRunProvider()
        self.prompt_addenda = prompt_addenda or {}
        self.state = state or WorkflowState(series=self.series, config=self.config)
        self.state.provider = self.provider.name

        for p in list_prompts(self.series):
            if p.id not in self.state.steps:
                self.state.steps[p.id] = StepRecord(
                    step_id=p.id, key=p.key, title=p.title, series_index=p.series_index
                )

    def run_step(self, step_id: int) -> StepRecord:
        definition = get_prompt(step_id)
        record = self.state.steps[step_id]
        record.started_at = _utc_now_iso()
        record.status = "running"
        record.error = None

        try:
            prompt_text = render_prompt(step_id, self.config, fallback_placeholder=True)
            addendum = self.prompt_addenda.get(step_id)
            if addendum:
                prompt_text = f"{prompt_text}\n\n{addendum}"
            record.prompt_rendered = prompt_text
            answer = self.provider.execute_step(definition, prompt_text, self.state)
        except Exception as exc:
            record.status = "failed"
            record.error = str(exc)
            record.completed_at = _utc_now_iso()
            raise

        if answer is None:
            record.status = "awaiting_response"
            record.completed_at = None
        else:
            record.output = answer
            record.status = "completed"
            record.completed_at = _utc_now_iso()
        self.state.updated_at = _utc_now_iso()
        return record

    def run_all(self, checkpoint_path: str | Path | None = None) -> WorkflowState:
        """Run pending steps in order. Stop at the first step that awaits a response."""
        for p in list_prompts(self.series):
            if self.state.steps[p.id].status == "completed":
                continue
            try:
                record = self.run_step(p.id)
            finally:
                if checkpoint_path:
                    self.state.save_checkpoint(checkpoint_path)
            if record.status == "awaiting_response":
                break
        return self.state

    def pending_steps(self) -> list[StepRecord]:
        return [
            self.state.steps[p.id]
            for p in list_prompts(self.series)
            if self.state.steps[p.id].status != "completed"
        ]

    def is_complete(self) -> bool:
        return not self.pending_steps()

    def export_manifest(self, output_dir: str | Path) -> dict[str, Path]:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        state_file = out / STATE_FILE
        self.state.save_checkpoint(state_file)

        topic = self.config.get("idea") or self.config.get("topic") or self.config.get("niche") or "N/A"
        lines = [
            f"# Content Pipeline Manifest ({self.series})",
            "",
            f"- Provider: `{self.state.provider}`",
            f"- Updated: `{self.state.updated_at}`",
            f"- Topic: `{topic}`",
            "",
            "| Prompt | Step | Title | Status |",
            "|:---|:---|:---|:---|",
        ]
        prompts = list_prompts(self.series)
        for p in prompts:
            rec = self.state.steps[p.id]
            lines.append(f"| {p.id:02d} | {p.series_index} | {p.title} | `{rec.status}` |")
        lines.append("")
        for p in prompts:
            rec = self.state.steps[p.id]
            lines.append(f"## Prompt {p.id:02d}: {p.title}")
            lines.append("")
            if rec.status == "completed":
                lines.append(rec.output)
            elif rec.error:
                lines.append(f"> FAILED: {rec.error}")
            else:
                lines.append(f"> {rec.status}")
            lines.append("")

        manifest_file = out / MANIFEST_FILE
        manifest_file.write_text("\n".join(lines), encoding="utf-8")
        return {"state": state_file, "manifest": manifest_file}
