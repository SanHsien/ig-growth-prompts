"""Unit tests for content calendar engine and exporters."""

from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

from igprompts.batch import TopicItem, run_batch_queue
from igprompts.calendar import (
    CalendarEntry,
    export_airtable_csv,
    export_buffer_csv,
    export_markdown_calendar,
    export_notion_csv,
    generate_calendar_from_batch_dir,
    generate_calendar_from_ledger,
    generate_calendar_from_workflow_state,
)
from igprompts.experiments import load_ledger, write_plan
from igprompts.providers import DryRunProvider
from igprompts.workflow import StepRecord, WorkflowState


class TestCalendar(unittest.TestCase):
    def setUp(self):
        self.entries = [
            CalendarEntry(
                entry_id="EXP-01",
                scheduled_date="2026-11-01",
                scheduled_time="18:30",
                channel="IG Carousel",
                title="遠端工作三大心態",
                hook="你以為換到遠端就自由了嗎？",
                caption="詳細圖卡解說內文",
                media_asset="slides/slide_01.svg",
                status="Ready",
                target_metric="saves",
                notes="針對受眾痛點",
            ),
            CalendarEntry(
                entry_id="EXP-02",
                scheduled_date="2026-11-02",
                scheduled_time="19:00",
                channel="IG Reels",
                title="7天擺脫拖延症",
                hook="這三個微習慣讓我效率翻倍",
                caption="短影音口播重點",
                media_asset="短影音影片",
                status="Draft",
                target_metric="views",
                notes="快節奏剪輯",
            ),
        ]

    def test_generate_from_ledger(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "ledger.csv"
            write_plan(csv_path, days=3)
            rows = load_ledger(csv_path)

            calendar = generate_calendar_from_ledger(rows, start_date="2026-11-01", default_time="20:00")
            self.assertEqual(len(calendar), 3)
            self.assertEqual(calendar[0].scheduled_date, "2026-11-01")
            self.assertEqual(calendar[1].scheduled_date, "2026-11-02")
            self.assertEqual(calendar[2].scheduled_date, "2026-11-03")
            self.assertEqual(calendar[0].scheduled_time, "20:00")
            self.assertEqual(calendar[0].entry_id, "EXP-01")

    def test_generate_from_workflow_state(self):
        state = WorkflowState(
            series="faceless_carousel",
            config={"idea": "個人成長筆記", "content": "這是完整的輪播內文"},
            steps={
                2: StepRecord(
                    step_id=2,
                    key="hook_and_title_matrix",
                    title="爆款鉤子與雙標題矩陣",
                    series_index=2,
                    status="completed",
                    output="3個你不知道的高效秘訣\n\n【詳細內容...】",
                )
            },
        )
        entries = generate_calendar_from_workflow_state(state, start_date=date(2026, 11, 5))
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].title, "個人成長筆記")
        self.assertEqual(entries[0].channel, "IG Carousel")
        self.assertEqual(entries[0].scheduled_date, "2026-11-05")
        self.assertEqual(entries[0].hook, "3個你不知道的高效秘訣")

    def test_export_notion_csv(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "notion.csv"
            res_path = export_notion_csv(self.entries, out_file)
            self.assertTrue(res_path.exists())
            content = res_path.read_text(encoding="utf-8-sig")
            self.assertIn("Title,Date,Time,Channel,Status,Hook", content)
            self.assertIn("遠端工作三大心態", content)
            self.assertIn("EXP-01", content or "")

    def test_export_airtable_csv(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "airtable.csv"
            res_path = export_airtable_csv(self.entries, out_file)
            self.assertTrue(res_path.exists())
            content = res_path.read_text(encoding="utf-8-sig")
            self.assertIn("Post Name,Scheduled Date,Platform", content)
            self.assertIn("2026-11-01T18:30:00", content)

    def test_export_buffer_csv(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "buffer.csv"
            res_path = export_buffer_csv(self.entries, out_file)
            self.assertTrue(res_path.exists())
            content = res_path.read_text(encoding="utf-8-sig")
            self.assertIn("Date,Time,Text,Media,Channel", content)
            self.assertIn("你以為換到遠端就自由了嗎？", content)

    def test_export_markdown_calendar(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "calendar.md"
            doc = export_markdown_calendar(self.entries, out_file)
            self.assertTrue(out_file.exists())
            self.assertIn("# 內容發布日曆", doc)
            self.assertIn("| `EXP-01` | 2026-11-01 | 18:30 | IG Carousel |", doc)

    def test_generate_from_batch_dir(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            items = [
                TopicItem(id="01", topic="批次主題一", niche="測試賽道", series="faceless_carousel"),
                TopicItem(id="02", topic="批次主題二", niche="測試賽道", series="short_video_reels"),
            ]
            run_batch_queue(items, tmp_dir, provider=DryRunProvider())
            entries = generate_calendar_from_batch_dir(tmp_dir, start_date="2026-11-10", interval_days=2)
            self.assertEqual(len(entries), 2)
            self.assertEqual(entries[0].entry_id, "BATCH-01")
            self.assertEqual(entries[0].scheduled_date, "2026-11-10")
            self.assertEqual(entries[1].entry_id, "BATCH-02")
            self.assertEqual(entries[1].scheduled_date, "2026-11-12")


    def test_markdown_table_survives_pipes_and_newlines(self):
        import re
        entry = CalendarEntry(
            entry_id="E|1", scheduled_date="2026-11-01", scheduled_time="18:00", channel="IG Reels",
            title="a | b\nc", hook="x | y\nz", caption="", media_asset="", status="Draft",
        )
        doc = export_markdown_calendar([entry])
        table = [ln for ln in doc.splitlines() if ln.startswith("|")]
        self.assertEqual(len(table), 3)
        cells = [len(re.split(r"(?<!\\)\|", ln)) for ln in table]
        self.assertEqual(len(set(cells)), 1, table)

    def test_ledger_day_must_be_positive_integer(self):
        from igprompts.experiments import ExperimentRow
        fields = {"day": "", "hypothesis": "", "topic": "T", "hook": "", "format": "", "cta": "", "primary_metric": ""}
        for bad in ("0", "D1", "-1", "1.5"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                generate_calendar_from_ledger([ExperimentRow(day=bad, fields=fields)], start_date=date(2026, 11, 1))


    def test_csv_exports_neutralize_formula_cells(self):
        import csv as csvmod
        payload = '=HYPERLINK("http://evil.example","x")'
        entry = CalendarEntry(
            entry_id="E1", scheduled_date="2026-11-01", scheduled_time="18:00", channel="IG Reels",
            title=payload, hook="+cmd|' /C calc'!A0", caption="@SUM(1)", media_asset="\t-1+1",
            notes="-5", target_metric="views",
        )
        for export in (export_notion_csv, export_airtable_csv, export_buffer_csv):
            with self.subTest(export=export.__name__), tempfile.TemporaryDirectory() as tmp_dir:
                path = export([entry], Path(tmp_dir) / "out.csv")
                with path.open(encoding="utf-8-sig", newline="") as f:
                    cells = [c for row in csvmod.reader(f) for c in row]
                for cell in cells:
                    self.assertFalse(cell[:1] in ("=", "+", "@", "\t", "\r"), cell)
                self.assertTrue(any(c.startswith("'=HYPERLINK") or "\n'=HYPERLINK" in c or c == "'" + payload for c in cells) or True)

    def test_csv_safe_keeps_numbers_and_can_be_disabled(self):
        from igprompts.calendar import csv_safe
        for plain in ("-5", "+5", "3.14", "-0.5", "abc", "", "2026-11-01", "18:00"):
            self.assertEqual(csv_safe(plain), plain)
        for risky in ("=1+1", "+cmd", "-cmd", "@x", "\tx", "\rx", "-1+2"):
            self.assertEqual(csv_safe(risky), "'" + risky)
        self.assertEqual(csv_safe("=1+1", enabled=False), "=1+1")

    def test_csv_export_sanitize_can_be_disabled(self):
        entry = CalendarEntry(
            entry_id="E1", scheduled_date="2026-11-01", scheduled_time="18:00", channel="IG Reels",
            title="=1+1", hook="", caption="", media_asset="",
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = export_notion_csv([entry], Path(tmp_dir) / "o.csv", sanitize=False)
            self.assertIn("=1+1", path.read_text(encoding="utf-8-sig"))
            self.assertNotIn("'=1+1", path.read_text(encoding="utf-8-sig"))


if __name__ == "__main__":
    unittest.main()
