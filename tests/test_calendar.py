"""Unit tests for content calendar engine and exporters."""

from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

from igprompts.calendar import (
    CalendarEntry,
    export_airtable_csv,
    export_buffer_csv,
    export_markdown_calendar,
    export_notion_csv,
    generate_calendar_from_ledger,
    generate_calendar_from_workflow_state,
)
from igprompts.experiments import load_ledger, write_plan
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


if __name__ == "__main__":
    unittest.main()
