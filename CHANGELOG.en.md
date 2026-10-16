English | [中文版](CHANGELOG.md)

# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 2026-10-17

### Added

- **Automated Workflow Engine (Phase 1)**:
  - `igprompts/workflow.py`: `WorkflowState`, `WorkflowRunner`, `DryRunProvider`, `CallableProvider`.
  - Supports step-level lifecycle tracking (pending, running, completed, failed), checkpoint persistence, and resumption (`--resume`).
  - Exports `pipeline_manifest.md` and `workflow_state.json`.
- **Local Vector SVG Carousel Generator (Phase 2)**:
  - `igprompts/renderer.py`: Zero external dependencies, pure stdlib generation of 1080x1350 (Instagram 4:5 vertical) dark-mode carousel slides.
- **CLI Enhancements**:
  - `python -m igprompts run-pipeline`: Execute the 5-step workflow runner with optional `--render-slides` visual output.
  - `python -m igprompts render-slides`: Generate SVG carousel cards directly from state or config.
- **Roadmap Documents**: Added bilingual roadmap specifications `ROADMAP.md` and `ROADMAP.en.md`.
- **Unit Tests Expanded**: Added `tests/test_workflow.py` and `tests/test_renderer.py`, raising test count to 24 tests.

- `igprompts` core package (Python stdlib-only, zero third-party dependencies):
  - Built-in metadata, variable resolution, and template rendering for 5 core prompts.
  - End-to-end pipeline synthesis via `pipeline` command.
- CLI interface:
  - `python -m igprompts list`: List prompt IDs, keys, titles, and required variables.
  - `python -m igprompts show <id>`: Inspect raw prompt templates.
  - `python -m igprompts render <id> [--json-file] [--var key=value]`: Render a customized prompt ready for Claude / ChatGPT.
  - `python -m igprompts pipeline [--json-file] [-o output.md]`: Export the 5-stage content production pipeline into Markdown.
- Sample inputs: `examples/sample_inputs.json` featuring an AI & software architecture scenario.
- Quality gates & developer tools:
  - `tools/dev_check.ps1`: Windows-native canonical quality check (unit tests, relative link verification, git whitespace checks).
  - `tools/check_links.py`: Local offline Markdown relative link and image resolver.
  - `.github/workflows/ci.yml`: Multi-platform CI pipeline (Windows pwsh + Ubuntu Python 3.10 / 3.13 matrix).
- Complete governance & bilingual documentation:
  - `AGENTS.md`: Canonical rules and single source of truth for AI agents.
  - `CLAUDE.md`: Claude-specific guidance and verification protocol.
  - `README.md` and `README.en.md`: Comprehensive bilingual documentation.
  - `CHANGELOG.md` and `CHANGELOG.en.md`: Bilingual version changelogs.
  - `LICENSE`: MIT License.
  - `.editorconfig` and `.gitattributes`: Strict LF and UTF-8 encoding enforcement across platforms.
- Test suite:
  - 15 unit tests covering models, prompt rendering, missing-variable validation, and CLI commands.
