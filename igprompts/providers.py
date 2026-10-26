"""Tool-agnostic execution providers.

The repository never hard-codes a model vendor. A provider only decides *how*
a rendered prompt reaches an AI tool and how the answer comes back:

- ``ManualProvider``  : file handoff. Works with any chat UI (Claude, ChatGPT,
                        Gemini, DeepSeek, Copilot, ...). Paste the prompt file,
                        save the answer next to it, rerun.
- ``CommandProvider`` : pipes the prompt to any CLI via stdin and reads stdout
                        (e.g. ``ollama run llama3``, ``llm``, ``claude -p``,
                        ``gemini``). The command is user-supplied.
- ``CallableProvider``: any Python function (SDK wrappers, agents, tests).
- ``DryRunProvider``  : calls nothing. Returns an explicit marker so a dry run
                        can never be mistaken for model output.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .models import PromptDefinition
    from .workflow import WorkflowState

DRY_RUN_MARKER = "[dry-run]"


class WorkflowProvider:
    """Contract: return the answer text, or ``None`` when the answer is not available yet."""

    name = "base"

    def execute_step(
        self, definition: PromptDefinition, prompt_text: str, state: WorkflowState
    ) -> str | None:
        raise NotImplementedError


class DryRunProvider(WorkflowProvider):
    """Offline verification only. Output is a marker, never fake content."""

    name = "dry-run"

    def execute_step(
        self, definition: PromptDefinition, prompt_text: str, state: WorkflowState
    ) -> str | None:
        return (
            f"{DRY_RUN_MARKER} Prompt {definition.id:02d} ({definition.key}) rendered, "
            f"{len(prompt_text)} chars. No AI tool was called."
        )


class ManualProvider(WorkflowProvider):
    """File handoff for any chat-based AI tool.

    For each step it writes ``NN-key.prompt.md``. The user pastes it into the
    tool of their choice and saves the answer as ``NN-key.response.md``.
    A missing or empty response file means the step is still waiting.
    """

    name = "manual"

    def __init__(self, handoff_dir: str | Path):
        self.handoff_dir = Path(handoff_dir)

    def paths(self, definition: PromptDefinition) -> tuple[Path, Path]:
        stem = f"{definition.id:02d}-{definition.key}"
        return (
            self.handoff_dir / f"{stem}.prompt.md",
            self.handoff_dir / f"{stem}.response.md",
        )

    def execute_step(
        self, definition: PromptDefinition, prompt_text: str, state: WorkflowState
    ) -> str | None:
        self.handoff_dir.mkdir(parents=True, exist_ok=True)
        prompt_path, response_path = self.paths(definition)
        prompt_path.write_text(prompt_text, encoding="utf-8")
        if not response_path.exists():
            return None
        answer = response_path.read_text(encoding="utf-8-sig").strip()
        return answer or None


class CommandProvider(WorkflowProvider):
    """Pipe the prompt to a user-supplied command through stdin.

    The command runs through the system shell so users can pass the exact
    string they already use in their terminal. Non-zero exit codes and empty
    output raise errors instead of being treated as answers.
    """

    name = "command"

    def __init__(self, command: str, *, timeout: float = 600.0, encoding: str = "utf-8"):
        if not command or not command.strip():
            raise ValueError("CommandProvider needs a non-empty command.")
        self.command = command
        self.timeout = timeout
        self.encoding = encoding

    def execute_step(
        self, definition: PromptDefinition, prompt_text: str, state: WorkflowState
    ) -> str | None:
        try:
            result = subprocess.run(
                self.command,
                shell=True,
                input=prompt_text.encode(self.encoding),
                capture_output=True,
                timeout=self.timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise TimeoutError(
                f"Command timed out after {self.timeout}s on prompt {definition.id:02d}: {self.command}"
            ) from exc

        stderr = result.stderr.decode(self.encoding, errors="replace").strip()
        if result.returncode != 0:
            raise RuntimeError(
                f"Command exited with code {result.returncode} on prompt {definition.id:02d}: {stderr}"
            )
        try:
            answer = result.stdout.decode(self.encoding).strip()
        except UnicodeDecodeError as exc:
            raise RuntimeError(
                f"Command output is not valid {self.encoding}. "
                "Set --encoding to the tool's output encoding."
            ) from exc
        if not answer:
            raise RuntimeError(f"Command returned empty output on prompt {definition.id:02d}.")
        return answer


class CallableProvider(WorkflowProvider):
    """Wrap any Python callable ``(definition, prompt_text, state) -> str | None``."""

    name = "callable"

    def __init__(self, callback: Callable[[PromptDefinition, str, WorkflowState], str | None]):
        self.callback = callback

    def execute_step(
        self, definition: PromptDefinition, prompt_text: str, state: WorkflowState
    ) -> str | None:
        return self.callback(definition, prompt_text, state)
