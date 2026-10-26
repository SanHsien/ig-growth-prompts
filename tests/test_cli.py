"""Unit tests for the CLI entry point."""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from igprompts.cli import main, parse_var_arguments


class TestCLI(unittest.TestCase):
    def test_parse_var_arguments(self):
        result = parse_var_arguments(["niche=Engineering", "audience=Developers"])
        self.assertEqual(result, {"niche": "Engineering", "audience": "Developers"})

    def test_parse_var_arguments_invalid(self):
        with self.assertRaises(ValueError):
            parse_var_arguments(["invalid_arg_without_equals"])

    def test_cli_list(self):
        f = io.StringIO()
        with redirect_stdout(f):
            code = main(["list"])
        self.assertEqual(code, 0)
        output = f.getvalue()
        self.assertIn("01", output)
        self.assertIn("12", output)
        self.assertIn("niche_ideation", output)
        self.assertIn("reels_07_matrix", output)

    def test_cli_show(self):
        f = io.StringIO()
        with redirect_stdout(f):
            code = main(["show", "01"])
        self.assertEqual(code, 0)
        self.assertIn("操盤 IG 超過 10 年的成長顧問", f.getvalue())

    def test_cli_render_with_var(self):
        f = io.StringIO()
        with redirect_stdout(f):
            code = main([
                "render", "01",
                "--var", "niche=AI",
                "--var", "audience=Engineers",
                "--var", "goal=Reach",
            ])
        self.assertEqual(code, 0)
        output = f.getvalue()
        self.assertIn("🎯 利基市場（Niche）= AI", output)

    def test_cli_pipeline(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            json_file = Path(tmp_dir) / "cfg.json"
            json_file.write_text(json.dumps({
                "niche": "Code",
                "audience": "Devs",
                "goal": "Grow",
                "idea": "Testing",
                "tone": "Direct",
                "content": "Draft",
                "voice": "Plain",
                "brand_voice": "Expert",
            }, ensure_ascii=False), encoding="utf-8")

            out_file = Path(tmp_dir) / "output.md"
            code = main(["pipeline", "-f", str(json_file), "-o", str(out_file)])
            self.assertEqual(code, 0)
            self.assertTrue(out_file.exists())
            content = out_file.read_text(encoding="utf-8")
            self.assertIn("# Content Pipeline: 圖文與不露臉精準留存體系", content)

    def test_cli_run_pipeline_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            json_file = Path(tmp_dir) / "cfg.json"
            json_file.write_text(json.dumps({
                "niche": "Code",
                "audience": "Devs",
                "goal": "Grow",
                "idea": "CLI Test",
                "tone": "Direct",
                "content": "Draft",
                "voice": "Plain",
                "brand_voice": "Expert",
            }, ensure_ascii=False), encoding="utf-8")

            out_dir = Path(tmp_dir) / "run_out"
            code = main(["run-pipeline", "-f", str(json_file), "-o", str(out_dir)])
            self.assertEqual(code, 0)
            self.assertTrue((out_dir / "workflow_state.json").exists())
            self.assertTrue((out_dir / "pipeline_manifest.md").exists())

    def test_cli_render_slides(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            spec_file = Path(tmp_dir) / "slides.md"
            spec_file.write_text("# 標題一\n內文說明\n---\n# 標題二\n第二頁", encoding="utf-8")
            out_dir = Path(tmp_dir) / "slides_out"
            code = main(["render-slides", "--from", str(spec_file), "-o", str(out_dir)])
            self.assertEqual(code, 0)
            self.assertTrue((out_dir / "slide_01.svg").exists())

    def test_cli_experiment_plan_and_report(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_file = Path(tmp_dir) / "ledger.csv"
            code_plan = main(["experiment", "plan", "--csv", str(csv_file)])
            self.assertEqual(code_plan, 0)
            self.assertTrue(csv_file.exists())

            # Fill one line with data
            content = (
                "day,hypothesis,topic,hook,format,cta,primary_metric,views,saves,shares,comments,profile_visits,follows,avg_watch_pct\n"
                "1,Hypo,Top,Hk,Fmt,Cta,views,500,10,5,2,10,1,50.0\n"
            )
            csv_file.write_text(content, encoding="utf-8-sig")

            rep_file = Path(tmp_dir) / "report.md"
            code_rep = main(["experiment", "report", "--csv", str(csv_file), "-o", str(rep_file)])
            self.assertEqual(code_rep, 0)
            self.assertTrue(rep_file.exists())

    def test_cli_calendar_from_ledger(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_file = Path(tmp_dir) / "ledger.csv"
            code_plan = main(["experiment", "plan", "--csv", str(csv_file)])
            self.assertEqual(code_plan, 0)

            notion_out = Path(tmp_dir) / "notion.csv"
            code_cal = main([
                "calendar",
                "generate",
                "--from-ledger", str(csv_file),
                "--start-date", "2026-11-01",
                "--format", "notion",
                "-o", str(notion_out),
            ])
            self.assertEqual(code_cal, 0)
            self.assertTrue(notion_out.exists())

    def test_cli_batch(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            queue_file = Path(tmp_dir) / "queue.json"
            queue_file.write_text(json.dumps([
                {"id": "B01", "topic": "主題一", "niche": "賽道", "series": "faceless"}
            ]), encoding="utf-8")

            batch_out = Path(tmp_dir) / "batch_out"
            code_batch = main(["batch", "run", "-f", str(queue_file), "-o", str(batch_out)])
            self.assertEqual(code_batch, 0)
            self.assertTrue((batch_out / "B01_faceless_carousel" / "pipeline_manifest.md").exists())

    def test_cli_calendar_from_batch(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            queue_file = Path(tmp_dir) / "queue.json"
            queue_file.write_text(json.dumps([
                {"id": "B01", "topic": "主題一", "niche": "賽道", "series": "faceless"}
            ]), encoding="utf-8")

            batch_out = Path(tmp_dir) / "batch_out"
            self.assertEqual(main(["batch", "run", "-f", str(queue_file), "-o", str(batch_out)]), 0)

            cal_out = Path(tmp_dir) / "cal_export"
            code_cal = main([
                "calendar",
                "generate",
                "--from-batch", str(batch_out),
                "--format", "markdown",
                "-o", str(cal_out / "calendar.md"),
            ])
            self.assertEqual(code_cal, 0)
            self.assertTrue((cal_out / "calendar.md").exists())


    def test_cli_calendar_csv_sanitize_flag(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_file = Path(tmp_dir) / "ledger.csv"
            main(["experiment", "plan", "--csv", str(csv_file), "--days", "1"])
            text = csv_file.read_text(encoding="utf-8-sig").replace("1,,,,,", '1,,=1+1,,,', 1)
            csv_file.write_text(text, encoding="utf-8-sig")
            safe = Path(tmp_dir) / "safe.csv"
            raw = Path(tmp_dir) / "raw.csv"
            base = ["calendar", "generate", "--from-ledger", str(csv_file), "--start-date", "2026-11-01", "--format", "notion"]
            self.assertEqual(main(base + ["-o", str(safe)]), 0)
            self.assertEqual(main(base + ["--no-csv-sanitize", "-o", str(raw)]), 0)
            self.assertIn("'=1+1", safe.read_text(encoding="utf-8-sig"))
            self.assertNotIn("'=1+1", raw.read_text(encoding="utf-8-sig"))


if __name__ == "__main__":
    unittest.main()
