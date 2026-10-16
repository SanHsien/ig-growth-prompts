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
        self.assertIn("niche_ideation", output)
        self.assertIn("authority_positioning", output)

    def test_cli_show(self):
        f = io.StringIO()
        with redirect_stdout(f):
            code = main(["show", "1"])
        self.assertEqual(code, 0)
        self.assertIn("操盤 IG 超過 10 年的成長顧問", f.getvalue())

    def test_cli_render_with_var(self):
        f = io.StringIO()
        with redirect_stdout(f):
            code = main([
                "render", "1",
                "--var", "niche=AI",
                "--var", "audience=Engineers",
                "--var", "goal=Reach",
            ])
        self.assertEqual(code, 0)
        output = f.getvalue()
        self.assertIn("🎯 利基市場（Niche）= AI", output)
        self.assertIn("👥 受眾（Audience）= Engineers", output)
        self.assertIn("🚩 目標（Goal）= Reach", output)

    def test_cli_render_missing_fail(self):
        err = io.StringIO()
        with redirect_stderr(err):
            code = main(["render", "1", "--var", "niche=AI"])
        self.assertEqual(code, 1)
        self.assertIn("missing required variables", err.getvalue())

    def test_cli_render_allow_missing(self):
        f = io.StringIO()
        with redirect_stdout(f):
            code = main(["render", "1", "--var", "niche=AI", "--allow-missing"])
        self.assertEqual(code, 0)
        self.assertIn("<audience>", f.getvalue())

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
            self.assertIn("# End-to-End Content Generation Pipeline", content)
            self.assertIn("Step 1: 利基市場防套路與原創點子", content)


if __name__ == "__main__":
    unittest.main()
