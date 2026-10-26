"""Phase 3: 7-day experiment ledger.

Flow: Prompt 12 plans the test -> ``plan`` writes a CSV ledger -> the user fills in
real numbers from the platform dashboard -> ``report`` computes rates and ranks ->
the report becomes the ``content_and_metrics`` input of Prompt 10.

Blank cells stay unknown (``None``), never zero. That mirrors Prompt 10's rule:
separate what the data proves from what it cannot show.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass, field
from pathlib import Path

from .core import md_cell

TEXT_COLUMNS = ("day", "hypothesis", "topic", "hook", "format", "cta", "primary_metric")
COUNT_COLUMNS = ("views", "saves", "shares", "comments", "profile_visits", "follows")
PERCENT_COLUMNS = ("avg_watch_pct",)
COLUMNS = TEXT_COLUMNS + COUNT_COLUMNS + PERCENT_COLUMNS

RATE_METRICS = {
    "save_rate": "saves",
    "share_rate": "shares",
    "comment_rate": "comments",
    "profile_visit_rate": "profile_visits",
    "follow_rate": "follows",
}
METRICS = ("views", "avg_watch_pct") + tuple(RATE_METRICS)
MIN_VIEWS_FOR_RATES = 1


class LedgerError(ValueError):
    """Raised for malformed ledger files."""


@dataclass
class ExperimentRow:
    day: str
    fields: dict[str, str]
    numbers: dict[str, float | None] = field(default_factory=dict)

    def metric(self, name: str) -> float | None:
        if name in ("views", "avg_watch_pct"):
            return self.numbers.get(name)
        source = RATE_METRICS[name]
        views = self.numbers.get("views")
        count = self.numbers.get(source)
        if views is None or count is None or views < MIN_VIEWS_FOR_RATES:
            return None
        return count / views


def _parse_number(raw: str, column: str, day: str) -> float | None:
    text = (raw or "").strip().replace(",", "")
    if not text:
        return None
    if text.endswith("%"):
        text = text[:-1].strip()
    try:
        value = float(text)
    except ValueError as exc:
        raise LedgerError(f"Day {day}: column '{column}' has a non-numeric value '{raw}'.") from exc
    if not math.isfinite(value):
        raise LedgerError(f"Day {day}: column '{column}' has a non-finite value '{raw}'.")
    if value < 0:
        raise LedgerError(f"Day {day}: column '{column}' is negative ({raw}).")
    if column in PERCENT_COLUMNS and value > 100:
        raise LedgerError(f"Day {day}: '{column}' must be 0-100, got {raw}.")
    return value


def write_plan(path: str | Path, days: int = 7, overwrite: bool = False) -> Path:
    """Write an empty ledger. Excel on Windows opens UTF-8 with BOM correctly."""
    p = Path(path)
    if p.exists() and not overwrite:
        raise FileExistsError(f"{p} already exists. Use --overwrite to replace it.")
    if days < 1:
        raise ValueError("days must be >= 1")
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(COLUMNS)
        for d in range(1, days + 1):
            writer.writerow([str(d)] + [""] * (len(COLUMNS) - 1))
    return p


def load_ledger(path: str | Path) -> list[ExperimentRow]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Ledger not found: {p}")
    with p.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        missing = [c for c in COLUMNS if c not in header]
        if missing:
            raise LedgerError(f"Ledger is missing columns: {', '.join(missing)}")
        rows: list[ExperimentRow] = []
        for raw in reader:
            day = (raw.get("day") or "").strip()
            if not day:
                continue
            primary = (raw.get("primary_metric") or "").strip()
            if primary and primary not in METRICS:
                raise LedgerError(
                    f"Day {day}: primary_metric '{primary}' is not one of {', '.join(METRICS)}."
                )
            fields = {c: (raw.get(c) or "").strip() for c in TEXT_COLUMNS}
            numbers = {
                c: _parse_number(raw.get(c, ""), c, day) for c in COUNT_COLUMNS + PERCENT_COLUMNS
            }
            rows.append(ExperimentRow(day=day, fields=fields, numbers=numbers))
    if not rows:
        raise LedgerError("Ledger has no rows.")
    return rows


def _fmt(metric: str, value: float | None) -> str:
    if value is None:
        return "—"
    if metric == "views":
        return f"{value:,.0f}"
    if metric == "avg_watch_pct":
        return f"{value:.1f}%"
    return f"{value * 100:.2f}%"


def build_report(rows: list[ExperimentRow]) -> str:
    """Markdown report: table, per-metric leaders, and explicit unknowns."""
    lines = [
        "# 7 天測試報告",
        "",
        f"- 測試支數：{len(rows)}",
        "- 「—」代表沒有數據，不是 0。",
        "",
        "| Day | 假設 | 形式 | 主要指標 | " + " | ".join(METRICS) + " |",
        "|:---|:---|:---|:---|" + "---:|" * len(METRICS),
    ]
    for r in rows:
        cells = " | ".join(_fmt(m, r.metric(m)) for m in METRICS)
        lines.append(
            f"| {md_cell(r.day)} | {md_cell(r.fields['hypothesis'] or '—')} | "
            f"{md_cell(r.fields['format'] or '—')} | "
            f"{md_cell(r.fields['primary_metric'] or '—')} | {cells} |"
        )

    lines += ["", "## 可以確定的結論（只比較有數據的支數）", ""]
    confirmed = 0
    for m in METRICS:
        scored = [(r, r.metric(m)) for r in rows if r.metric(m) is not None]
        if len(scored) < 2:
            continue
        scored.sort(key=lambda x: x[1], reverse=True)
        best, worst = scored[0], scored[-1]
        lines.append(
            f"- **{m}**：最高 Day {best[0].day}（{_fmt(m, best[1])}，{best[0].fields['format'] or '形式未填'}），"
            f"最低 Day {worst[0].day}（{_fmt(m, worst[1])}），共 {len(scored)} 支有數據。"
        )
        confirmed += 1
    if not confirmed:
        lines.append("- 沒有任何指標同時有 2 支以上的數據，目前不能下比較結論。")

    lines += ["", "## 數據看不出來、不能亂猜的地方", ""]
    unknowns = 0
    for r in rows:
        gaps = [m for m in METRICS if r.metric(m) is None]
        if gaps:
            lines.append(f"- Day {r.day} 缺：{', '.join(gaps)}")
            unknowns += 1
        primary = r.fields["primary_metric"]
        if primary and r.metric(primary) is None:
            lines.append(f"  - Day {r.day} 的主要指標 `{primary}` 沒有數據，這支的假設尚未驗證。")
    if not unknowns:
        lines.append("- 所有欄位都有數據。")
    lines += [
        "- 每種形式只有 1 支樣本時，差異可能來自題目或發文時段，不能直接歸因於形式。",
        "",
    ]
    return "\n".join(lines)
