"""Unit tests for desktop GUI workbench module."""

from __future__ import annotations

import unittest
from pathlib import Path

from igprompts.cli import build_parser
from igprompts.gui import (
    THEMES,
    TK_AVAILABLE,
    build_command_provider,
    build_scheduler_script,
    detect_system_theme,
)


class TestGUI(unittest.TestCase):
    def test_gui_subcommand_registered(self):
        parser = build_parser()
        args = parser.parse_args(["gui"])
        self.assertEqual(args.command, "gui")

    def test_tkinter_module_presence(self):
        self.assertIsInstance(TK_AVAILABLE, bool)

    def test_theme_definitions(self):
        self.assertIn("dark", THEMES)
        self.assertIn("light", THEMES)
        required_keys = ["bg", "panel", "fg", "accent", "console_bg"]
        for key in required_keys:
            self.assertIn(key, THEMES["dark"])
            self.assertIn(key, THEMES["light"])

    def test_detect_system_theme_returns_valid_value(self):
        theme = detect_system_theme()
        self.assertIn(theme, ["dark", "light"])


    def test_scheduler_script_quotes_paths_and_sets_codepage(self):
        script = build_scheduler_script(Path("C:/My Output/batch out"), Path("C:/My Projects/igp"))
        self.assertIn("chcp 65001", script)
        self.assertIn('-o "C:/My Output/batch out"', script.replace("\\", "/"))
        self.assertIn('--from-batch "C:/My Output/batch out"', script.replace("\\", "/"))

    def test_command_provider_requires_configured_command(self):
        import os
        from unittest import mock
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("IGPROMPTS_LLM_CMD", None)
            with self.assertRaises(ValueError):
                build_command_provider()
        with mock.patch.dict(os.environ, {"IGPROMPTS_LLM_CMD": "mytool -p"}):
            self.assertEqual(build_command_provider().command, "mytool -p")

    @unittest.skipUnless(TK_AVAILABLE, "tkinter not available")
    def test_calendar_export_gives_every_series_a_unique_id(self):
        import tempfile
        from types import SimpleNamespace
        from unittest import mock
        from igprompts import gui
        from igprompts.batch import TopicItem, run_batch_queue
        from igprompts.providers import DryRunProvider

        with tempfile.TemporaryDirectory() as tmp:
            for series in ("faceless_carousel", "short_video_reels"):
                run_batch_queue([TopicItem(id="x", topic="t", series=series)], Path(tmp) / "tmp_batch")
                (Path(tmp) / series).mkdir()
                src = Path(tmp) / "tmp_batch" / f"x_{series}" / "workflow_state.json"
                (Path(tmp) / series / "workflow_state.json").write_bytes(src.read_bytes())
            stub = SimpleNamespace(
                ent_out=SimpleNamespace(get=lambda: tmp),
                ent_cal_date=SimpleNamespace(get=lambda: "2026-11-01"),
            )
            with mock.patch.object(gui, "messagebox") as mb:
                gui.IGPromptsGUI._export_calendar(stub, "notion")
                self.assertFalse(mb.showerror.called, mb.showerror.call_args)
            csv_text = (Path(tmp) / "calendar_export" / "notion_database.csv").read_text(encoding="utf-8-sig")
            ids = [ln.split(",")[0] for ln in csv_text.splitlines()[1:]]
            self.assertEqual(len(ids), 2)
            self.assertEqual(len(set(ids)), 2, ids)


if __name__ == "__main__":
    unittest.main()
