"""Unit tests for the SVG renderer and slide spec parser."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from igprompts.renderer import (
    SlideData,
    SlideSpecError,
    extract_slides_block,
    parse_slide_spec,
    render_slides_from_answer,
    render_slides_from_spec_file,
    render_svg_card,
    wrap_line,
)


class TestRenderer(unittest.TestCase):
    def test_wrap_line(self):
        lines = wrap_line("這是一段很長很長的中文測試句子用來驗證換行演算法是否正常運作", width=20)
        self.assertTrue(len(lines) > 1)

    def test_parse_slide_spec_success(self):
        spec = """# 封面標題
第一行說明
第二行說明

---

# 內頁標題
內文重點
"""
        slides = parse_slide_spec(spec)
        self.assertEqual(len(slides), 2)
        self.assertEqual(slides[0].title, "封面標題")
        self.assertTrue(slides[0].is_cover)
        self.assertFalse(slides[0].is_last)
        self.assertEqual(slides[1].title, "內頁標題")
        self.assertTrue(slides[1].is_last)

    def test_parse_slide_spec_missing_title(self):
        spec = "沒有以井號開頭的標題\n只有內文"
        with self.assertRaises(SlideSpecError):
            parse_slide_spec(spec)

    def test_extract_and_render_slides_from_answer(self):
        answer = """這是一段 AI 回應...

```slides
# 標題一
內文一

---

# 標題二
內文二
```
最後總結...
"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            files = render_slides_from_answer(answer, tmp_dir)
            self.assertEqual(len(files), 2)
            self.assertTrue(files[0].exists())

    def test_render_slides_without_block_raises(self):
        answer = "沒有 slides 區塊的回覆"
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self.assertRaises(SlideSpecError):
                render_slides_from_answer(answer, tmp_dir)


if __name__ == "__main__":
    unittest.main()
