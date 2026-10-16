"""Unit tests for prompt models and core rendering functions across all series."""

from __future__ import annotations

import unittest

from igprompts.core import (
    SERIES_FACELESS,
    SERIES_REELS,
    get_prompt,
    list_prompts,
    normalize_series,
    render_pipeline,
    render_prompt,
)


class TestPromptCore(unittest.TestCase):
    def test_list_prompts_all(self):
        prompts = list_prompts()
        self.assertEqual(len(prompts), 12)
        self.assertEqual([p.id for p in prompts], list(range(1, 13)))

    def test_list_prompts_by_series(self):
        faceless = list_prompts(SERIES_FACELESS)
        self.assertEqual(len(faceless), 5)
        self.assertEqual([p.id for p in faceless], [1, 2, 3, 4, 5])

        reels = list_prompts(SERIES_REELS)
        self.assertEqual(len(reels), 7)
        self.assertEqual([p.id for p in reels], list(range(6, 13)))

    def test_normalize_series_aliases(self):
        self.assertEqual(normalize_series("faceless"), SERIES_FACELESS)
        self.assertEqual(normalize_series("reels"), SERIES_REELS)
        self.assertEqual(normalize_series("claude_ig"), SERIES_FACELESS)
        self.assertEqual(normalize_series("chatgpt_reels"), SERIES_REELS)
        with self.assertRaises(ValueError):
            normalize_series("unknown_series")

    def test_get_prompt_valid(self):
        p1 = get_prompt(1)
        self.assertEqual(p1.id, 1)
        self.assertEqual(p1.key, "niche_ideation")

        p6 = get_prompt(6)
        self.assertEqual(p6.id, 6)
        self.assertEqual(p6.key, "reels_01_topics")
        self.assertIn("followers", p6.variables)

        p_str = get_prompt("06")
        self.assertEqual(p_str.id, 6)

        p_key = get_prompt("reels_07_matrix")
        self.assertEqual(p_key.id, 12)

    def test_get_prompt_invalid(self):
        with self.assertRaises(KeyError):
            get_prompt(99)
        with self.assertRaises(KeyError):
            get_prompt("nonexistent_key")

    def test_render_prompt_success(self):
        vars_dict = {
            "niche": "軟體架構",
            "audience": "後端工程師",
            "goal": "建立高信任度",
        }
        rendered = render_prompt(1, vars_dict)
        self.assertIn("🎯 利基市場（Niche）= 軟體架構", rendered)
        self.assertIn("👥 受眾（Audience）= 後端工程師", rendered)
        self.assertIn("🚩 目標（Goal）= 建立高信任度", rendered)

    def test_render_prompt_missing_variables_raises(self):
        with self.assertRaises(ValueError) as ctx:
            render_prompt(1, {"niche": "AI"})
        self.assertIn("audience", str(ctx.exception))
        self.assertIn("goal", str(ctx.exception))

    def test_render_prompt_fallback_placeholder(self):
        rendered = render_prompt(1, {"niche": "AI"}, fallback_placeholder=True)
        self.assertIn("🎯 利基市場（Niche）= AI", rendered)
        self.assertIn("👥 受眾（Audience）= <audience>", rendered)
        self.assertIn("🚩 目標（Goal）= <goal>", rendered)

    def test_render_pipeline(self):
        sample_config = {
            "niche": "AI",
            "audience": "Devs",
            "goal": "Reach",
            "idea": "Testing",
            "tone": "Plain",
            "content": "Draft",
            "voice": "Plain",
            "brand_voice": "Expert",
        }
        doc = render_pipeline(sample_config, series=SERIES_FACELESS)
        self.assertIn("# Content Pipeline: 圖文與不露臉精準留存體系", doc)
        self.assertIn("Prompt 01", doc)
        self.assertIn("Prompt 05", doc)


if __name__ == "__main__":
    unittest.main()
