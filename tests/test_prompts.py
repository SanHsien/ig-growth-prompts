"""Unit tests for prompt models and core rendering functions."""

from __future__ import annotations

import unittest

from igprompts.core import get_prompt, list_prompts, render_pipeline, render_prompt


class TestPromptCore(unittest.TestCase):
    def test_list_prompts(self):
        prompts = list_prompts()
        self.assertEqual(len(prompts), 5)
        self.assertEqual([p.id for p in prompts], [1, 2, 3, 4, 5])

    def test_get_prompt_valid(self):
        p1 = get_prompt(1)
        self.assertEqual(p1.id, 1)
        self.assertEqual(p1.key, "niche_ideation")
        self.assertIn("niche", p1.variables)
        self.assertIn("audience", p1.variables)
        self.assertIn("goal", p1.variables)

    def test_get_prompt_invalid(self):
        with self.assertRaises(KeyError):
            get_prompt(99)

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
        self.assertIn("列出 7 種觀眾已經看膩", rendered)

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
            "niche": "Niche A",
            "audience": "Audience B",
            "goal": "Goal C",
            "idea": "Idea D",
            "tone": "Tone E",
            "content": "Content F",
            "voice": "Voice G",
            "brand_voice": "Voice H",
        }
        doc = render_pipeline(sample_config)
        self.assertIn("# End-to-End Content Generation Pipeline", doc)
        self.assertIn("## Step 1: 利基市場防套路與原創點子", doc)
        self.assertIn("## Step 5: 不吹噓的個人品牌專業權威改寫", doc)
        self.assertIn("Niche A", doc)


if __name__ == "__main__":
    unittest.main()
