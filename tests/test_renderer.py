"""Unit tests for the SVG renderer."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from igprompts.renderer import SlideData, generate_carousel_from_workflow, render_svg_card
from igprompts.workflow import WorkflowState


class TestRenderer(unittest.TestCase):
    def test_render_svg_card_content(self):
        slide = SlideData(
            title="測試封面標題",
            body_lines=["第一行文字說明", "第二行文字說明"],
            page=1,
            total=5,
            is_cover=True,
        )
        svg = render_svg_card(slide)
        self.assertIn("<svg", svg)
        self.assertIn("viewBox=\"0 0 1080 1350\"", svg)
        self.assertIn("測試封面標題", svg)
        self.assertIn("第一行文字說明", svg)
        self.assertIn("1 / 5", svg)

    def test_generate_carousel_from_workflow(self):
        state = WorkflowState(config={"idea": "SVG Test Topic"})
        with tempfile.TemporaryDirectory() as tmp_dir:
            files = generate_carousel_from_workflow(state, tmp_dir)
            self.assertEqual(len(files), 5)
            for f in files:
                self.assertTrue(f.exists())
                text = f.read_text(encoding="utf-8")
                self.assertTrue(text.startswith("<svg"))
                self.assertTrue(text.strip().endswith("</svg>"))


if __name__ == "__main__":
    unittest.main()
