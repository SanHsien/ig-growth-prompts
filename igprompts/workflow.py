"""Workflow state machine, execution engine, and pluggable providers."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .core import get_prompt, list_prompts, render_prompt


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class StepRecord:
    step_id: int
    title: str
    prompt_rendered: str = ""
    output: str = ""
    status: str = "pending"  # pending, running, completed, failed, skipped
    started_at: str | None = None
    completed_at: str | None = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowState:
    config: dict[str, Any] = field(default_factory=dict)
    steps: dict[int, StepRecord] = field(default_factory=dict)
    created_at: str = field(default_factory=_utc_now_iso)
    updated_at: str = field(default_factory=_utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "config": self.config,
            "steps": {str(k): asdict(v) for k, v in self.steps.items()},
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkflowState:
        state = cls(
            config=data.get("config", {}),
            created_at=data.get("created_at", _utc_now_iso()),
            updated_at=data.get("updated_at", _utc_now_iso()),
        )
        raw_steps = data.get("steps", {})
        for k, v in raw_steps.items():
            state.steps[int(k)] = StepRecord(**v)
        return state

    def save_checkpoint(self, path: str | Path) -> None:
        self.updated_at = _utc_now_iso()
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def load_checkpoint(cls, path: str | Path) -> WorkflowState:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Checkpoint file not found: {p}")
        data = json.loads(p.read_text(encoding="utf-8"))
        return cls.from_dict(data)


class WorkflowProvider:
    """Base interface for step execution."""

    def execute_step(self, step_id: int, prompt_text: str, state: WorkflowState) -> str:
        raise NotImplementedError


class DryRunProvider(WorkflowProvider):
    """Deterministic, offline provider for simulation and local verification."""

    def execute_step(self, step_id: int, prompt_text: str, state: WorkflowState) -> str:
        cfg = state.config
        niche = cfg.get("niche", "個人品牌")
        idea = cfg.get("idea", "爆款內容經營")

        if step_id == 1:
            return (
                f"【分析利基市場：{niche}】\n"
                "1. 看膩套路：每日打卡無乾貨、空泛雞湯、流水帳日常、秀存款截圖、無結論說教...\n"
                f"2. 推薦 Top 3 選題：\n"
                f"   - 第 1 名：工程師不靠運氣的 3 階段複利系統（主軸：系統化思維，格式：輪播貼文）\n"
                f"   - 第 2 名：為什麼 90% 認真的人在 IG 做白工？（主軸：認知盲點，格式：純字幕短片）\n"
                f"   - 第 3 名：零露臉、零剪輯的純文字經營指南（主軸：降摩擦力，格式：無聲圖卡）"
            )
        elif step_id == 2:
            return (
                f"【15 句爆款 Hook 生成（主題：{idea}）】\n"
                "1. 懸念型：這 3 個隱藏指標，決定了你的貼文會不會爆。（9字）\n"
                "2. 逆向型：越努力日更，演算法越容易放棄你。（15字）\n"
                "3. 情緒型：寫了一整天卻沒人看，問題不在文筆。（15字）\n"
                "4. 數據型：同一個選題換句開頭，完播率差 40%。（15字）\n"
                "5. 內行型：高手看 IG 後台，只看收藏與分享率。（15字）\n"
                "最強 5 句排序推薦已標注理由。"
            )
        elif step_id == 3:
            return (
                "【3 種不露臉版本完整腳本】\n"
                "版本一：5 頁輪播貼文（Dark Mode 深色大字、留白、層次分明）\n"
                "  P1（封面）：越努力日更，演算法越容易放棄你。\n"
                "  P2（痛點）：盲目日更只會稀釋權重，演算法評估的是完讀率而非頻率。\n"
                "  P3（解法）：建立滑梯文案結構，每行收尾埋下一個誘因。\n"
                "  P4（複利）：以高收藏價值為核心，做讀者半年後還能查閱的工具卡。\n"
                "  P5（CTA）：收藏這張卡片，下次動筆前逐項檢核。\n"
                "版本二：純字幕 Reel（黑底白字節奏快切）\n"
                "版本三：無聲極簡圖文"
            )
        elif step_id == 4:
            return (
                "【留存與完讀率改寫完成】\n"
                "刪除 6 處軟弱句與開頭廢話，調整行距與節奏，每行結尾加入順承引導詞。\n"
                "改動清單：\n"
                "- 原句：「我覺得大家可能在做的時候會有些忽略...」-> 改為「90% 的人忽略了一件事：」\n"
                "- 原句：「以上就是我想分享的希望有幫助」-> 改為「存下這篇，下次寫文直接套用。」"
            )
        elif step_id == 5:
            return (
                "【建立權威感 3 版本】\n"
                "1. 質感版：文字節奏放慢，以真實除錯細節代入，字句留白，散發從容底氣。\n"
                "2. 俐落版：句子短、動詞主導、直接切中要害，適合 Threads 與快節奏閱讀。\n"
                "3. 高級版：字字克制，不堆砌數字與光環，用精確的底層原理建立信服感。"
            )
        return f"Step {step_id} completed."


class CallableProvider(WorkflowProvider):
    """Provider powered by a custom Python callable."""

    def __init__(self, callback: Callable[[int, str, WorkflowState], str]):
        self.callback = callback

    def execute_step(self, step_id: int, prompt_text: str, state: WorkflowState) -> str:
        return self.callback(step_id, prompt_text, state)


class WorkflowRunner:
    """Executes the pipeline stages, tracks state, and persists artifacts."""

    def __init__(
        self,
        config: dict[str, Any],
        provider: WorkflowProvider | None = None,
        state: WorkflowState | None = None,
    ):
        self.config = config
        self.provider = provider or DryRunProvider()
        self.state = state or WorkflowState(config=config)

        # Initialize any missing steps
        for p in list_prompts():
            if p.id not in self.state.steps:
                self.state.steps[p.id] = StepRecord(
                    step_id=p.id,
                    title=p.title,
                )

    def run_step(self, step_id: int) -> StepRecord:
        definition = get_prompt(step_id)
        record = self.state.steps[step_id]

        record.started_at = _utc_now_iso()
        record.status = "running"
        record.error = None

        try:
            prompt_text = render_prompt(step_id, self.config, fallback_placeholder=True)
            record.prompt_rendered = prompt_text
            output_text = self.provider.execute_step(step_id, prompt_text, self.state)
            record.output = output_text
            record.status = "completed"
            record.completed_at = _utc_now_iso()
        except Exception as e:
            record.status = "failed"
            record.error = str(e)
            record.completed_at = _utc_now_iso()
            raise

        self.state.updated_at = _utc_now_iso()
        return record

    def run_all(
        self,
        start_step: int = 1,
        end_step: int = 5,
        checkpoint_path: str | Path | None = None,
    ) -> WorkflowState:
        for step_id in range(start_step, end_step + 1):
            if step_id in self.state.steps and self.state.steps[step_id].status == "completed":
                continue
            self.run_step(step_id)
            if checkpoint_path:
                self.state.save_checkpoint(checkpoint_path)
        return self.state

    def export_manifest(self, output_dir: str | Path) -> dict[str, Path]:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        # 1. State JSON
        state_file = out / "workflow_state.json"
        self.state.save_checkpoint(state_file)

        # 2. Markdown Summary Manifest
        manifest_file = out / "pipeline_manifest.md"
        manifest_lines = [
            "# Content Production Pipeline Manifest",
            "",
            f"- Generated at: `{self.state.updated_at}`",
            f"- Topic: `{self.config.get('idea', self.config.get('niche', 'N/A'))}`",
            "",
            "## Execution Overview",
            "",
            "| Step | Title | Status | Completed At |",
            "|:---|:---|:---|:---|",
        ]
        for p in list_prompts():
            rec = self.state.steps.get(p.id)
            status = rec.status if rec else "pending"
            completed = rec.completed_at if rec else "-"
            manifest_lines.append(f"| {p.id} | {p.title} | `{status}` | {completed} |")

        manifest_lines.append("\n---\n")
        for p in list_prompts():
            rec = self.state.steps.get(p.id)
            manifest_lines.append(f"### Step {p.id}: {p.title}\n")
            if rec and rec.output:
                manifest_lines.append("#### Output Deliverable\n")
                manifest_lines.append(rec.output)
            manifest_lines.append("\n---\n")

        manifest_file.write_text("\n".join(manifest_lines), encoding="utf-8")

        return {
            "state": state_file,
            "manifest": manifest_file,
        }
