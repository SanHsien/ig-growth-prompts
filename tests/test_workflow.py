"""Unit tests for workflow runner, providers, and state machine."""

from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import MagicMock, patch

from igprompts.cli import main
from igprompts.core import SERIES_FACELESS, SERIES_REELS, get_prompt
from igprompts.models import PromptDefinition
from igprompts.providers import CallableProvider, DryRunProvider, ManualProvider
from igprompts.workflow import STATE_FILE, WorkflowRunner, WorkflowState


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

    def _assert_failed_checkpoint_can_resume(self, failure):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out = Path(tmp_dir) / "workflow with spaces"
            ckpt = out / STATE_FILE
            runner = WorkflowRunner(config={"niche": "續跑驗證"})
            first = runner.run_step(1).output
            runner.state.save_checkpoint(ckpt)
            previous = ckpt.read_bytes()
            runner.run_step(2)

            with failure, self.assertRaisesRegex(OSError, "injected"):
                runner.state.save_checkpoint(ckpt)

            self.assertEqual(ckpt.read_bytes(), previous)
            loaded = WorkflowState.load_checkpoint(ckpt)
            self.assertEqual(loaded.steps[1].output, first)
            self.assertEqual(loaded.steps[2].status, "pending")
            self.assertEqual(list(out.iterdir()), [ckpt])

            executed = []
            execute = DryRunProvider.execute_step

            def track(provider, definition, prompt, state):
                executed.append(definition.id)
                return execute(provider, definition, prompt, state)

            with patch.object(DryRunProvider, "execute_step", track), redirect_stdout(io.StringIO()):
                code = main(["run-pipeline", "--resume", "--provider", "dry-run", "-o", str(out)])
            self.assertEqual(code, 0)
            self.assertEqual(executed, [2, 3, 4, 5])
            resumed = WorkflowState.load_checkpoint(ckpt)
            self.assertTrue(all(step.status == "completed" for step in resumed.steps.values()))
            self.assertEqual(resumed.steps[1].output, first)

    def test_checkpoint_partial_write_failure_preserves_state_and_resume(self):
        real_open = io.open

        def failing_open(*args, **kwargs):
            stream = real_open(*args, **kwargs)
            if "w" not in stream.mode:
                return stream
            wrapped = MagicMock(wraps=stream)
            wrapped.__enter__.return_value = wrapped
            wrapped.__exit__.side_effect = stream.__exit__

            def partial_write(text):
                stream.write(text[:7])
                stream.flush()
                raise OSError("injected partial write failure")

            wrapped.write.side_effect = partial_write
            return wrapped

        self._assert_failed_checkpoint_can_resume(patch("io.open", side_effect=failing_open))

    def test_checkpoint_replace_failure_preserves_state_and_resume(self):
        def fail_replace(source, target):
            self.assertEqual(source.parent.resolve(), target.parent.resolve())
            self.assertNotEqual(source, target)
            staged = WorkflowState.load_checkpoint(source)
            self.assertEqual(staged.steps[2].status, "completed")
            raise OSError("injected replace failure")

        self._assert_failed_checkpoint_can_resume(
            patch.object(Path, "replace", autospec=True, side_effect=fail_replace)
        )

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


    def test_manual_response_with_utf8_bom_is_clean(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            provider = ManualProvider(tmp_dir)
            definition = get_prompt(1)
            _, response_path = provider.paths(definition)
            response_path.write_bytes(b"\xef\xbb\xbfanswer text\n")
            answer = provider.execute_step(definition, "prompt", WorkflowState())
            self.assertEqual(answer, "answer text")


if __name__ == "__main__":
    unittest.main()
