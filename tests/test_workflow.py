"""Unit tests for workflow runner, providers, and state machine."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from igprompts.core import SERIES_FACELESS, SERIES_REELS, get_prompt
from igprompts.models import PromptDefinition
from igprompts.providers import CallableProvider, DryRunProvider, ManualProvider
from igprompts.workflow import WorkflowRunner, WorkflowState


class TestWorkflow(unittest.TestCase):
    def test_workflow_state_serialization(self):
        state = WorkflowState(series=SERIES_FACELESS, config={"niche": "AI"})
        d = state.to_dict()
        self.assertEqual(d["config"]["niche"], "AI")
        self.assertEqual(d["series"], SERIES_FACELESS)

        restored = WorkflowState.from_dict(d)
        self.assertEqual(restored.config["niche"], "AI")
        self.assertEqual(restored.series, SERIES_FACELESS)

    def test_workflow_checkpoint_persistence(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            ckpt = Path(tmp_dir) / "state.json"
            state = WorkflowState(series=SERIES_REELS, config={"idea": "Topic A"})
            state.save_checkpoint(ckpt)
            self.assertTrue(ckpt.exists())

            loaded = WorkflowState.load_checkpoint(ckpt)
            self.assertEqual(loaded.config["idea"], "Topic A")
            self.assertEqual(loaded.series, SERIES_REELS)

    def test_workflow_runner_dry_run_faceless(self):
        config = {
            "niche": "AI 自動化",
            "audience": "開發者",
            "goal": "建立個人品牌",
            "idea": "IG 經營",
            "tone": "自然",
            "content": "草稿內容",
            "voice": "理性",
            "brand_voice": "低調行家",
        }
        runner = WorkflowRunner(config=config, series=SERIES_FACELESS, provider=DryRunProvider())
        state = runner.run_all()

        self.assertEqual(len(state.steps), 5)
        for i in range(1, 6):
            self.assertEqual(state.steps[i].status, "completed")
            self.assertIn("[dry-run]", state.steps[i].output)

    def test_workflow_runner_dry_run_reels(self):
        config = {
            "niche": "軟體工程",
            "audience": "工程師",
            "followers": "1000",
            "stage_goal": "觸及",
            "topic": "短影音主題",
            "trend": "反差對比",
            "content_and_metrics": "數據與腳本",
            "goal": "破千粉",
            "daily_count": "1",
            "formats": "純字幕、口播",
        }
        runner = WorkflowRunner(config=config, series=SERIES_REELS, provider=DryRunProvider())
        state = runner.run_all()

        self.assertEqual(len(state.steps), 7)
        for i in range(6, 13):
            self.assertEqual(state.steps[i].status, "completed")
            self.assertIn("[dry-run]", state.steps[i].output)

    def test_manual_provider_flow(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            handoff = Path(tmp_dir) / "handoff"
            provider = ManualProvider(handoff)
            p1 = get_prompt(1)

            state = WorkflowState(series=SERIES_FACELESS, config={"niche": "Testing"})
            # Step 1: No response file -> status awaiting_response
            res = provider.execute_step(p1, "Prompt Text", state)
            self.assertIsNone(res)
            prompt_file, response_file = provider.paths(p1)
            self.assertTrue(prompt_file.exists())

            # Step 2: Write answer to response file
            response_file.write_text("My AI Answer", encoding="utf-8")
            res_after = provider.execute_step(p1, "Prompt Text", state)
            self.assertEqual(res_after, "My AI Answer")


if __name__ == "__main__":
    unittest.main()
