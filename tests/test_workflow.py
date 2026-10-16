"""Unit tests for the workflow engine, state machine, and providers."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from igprompts.workflow import CallableProvider, DryRunProvider, WorkflowRunner, WorkflowState


class TestWorkflow(unittest.TestCase):
    def test_workflow_state_serialization(self):
        state = WorkflowState(config={"niche": "AI"})
        d = state.to_dict()
        self.assertEqual(d["config"]["niche"], "AI")

        restored = WorkflowState.from_dict(d)
        self.assertEqual(restored.config["niche"], "AI")

    def test_workflow_checkpoint_persistence(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            ckpt = Path(tmp_dir) / "state.json"
            state = WorkflowState(config={"idea": "Topic A"})
            state.save_checkpoint(ckpt)
            self.assertTrue(ckpt.exists())

            loaded = WorkflowState.load_checkpoint(ckpt)
            self.assertEqual(loaded.config["idea"], "Topic A")

    def test_workflow_runner_dry_run(self):
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
        runner = WorkflowRunner(config=config, provider=DryRunProvider())
        state = runner.run_all()

        self.assertEqual(len(state.steps), 5)
        for i in range(1, 6):
            self.assertEqual(state.steps[i].status, "completed")
            self.assertTrue(len(state.steps[i].output) > 0)
            self.assertIsNotNone(state.steps[i].completed_at)

    def test_workflow_runner_callable_provider(self):
        def mock_llm(step_id: int, prompt_text: str, state: WorkflowState) -> str:
            return f"Mock response for step {step_id}"

        runner = WorkflowRunner(config={"niche": "Test"}, provider=CallableProvider(mock_llm))
        rec = runner.run_step(1)
        self.assertEqual(rec.output, "Mock response for step 1")
        self.assertEqual(rec.status, "completed")

    def test_export_manifest(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            runner = WorkflowRunner(config={"idea": "Manifest Test"}, provider=DryRunProvider())
            runner.run_all()
            artifacts = runner.export_manifest(tmp_dir)

            self.assertTrue(artifacts["state"].exists())
            self.assertTrue(artifacts["manifest"].exists())
            manifest_text = artifacts["manifest"].read_text(encoding="utf-8")
            self.assertIn("# Content Production Pipeline Manifest", manifest_text)
            self.assertIn("Step 1: 利基市場防套路與原創點子", manifest_text)


if __name__ == "__main__":
    unittest.main()
