English | [中文版](CHANGELOG.md)

# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 2026-10-17

### Added

- **Short-Form Video & Reels System (Prompts 06 ~ 12)**:
  - Curated all 7 short-form video prompts: `06-reels-7day-topics.md` through `12-reels-seven-day-test-matrix.md`.
  - Covers 7-day topics, 1-3s hooks, retention scripts, viral sharing, data diagnosis, strategic trends, and 7-day test tables.
- **Unified 01-12 IDs & Model-Agnostic Architecture**:
  - Unified numbering from 01 to 12 across the entire repository to resolve numbering collisions.
  - Neutral series identifiers: `faceless_carousel` and `short_video_reels`.
  - Fully compatible with any user-preferred AI tool (ChatGPT, Claude, Gemini, DeepSeek, Ollama, custom agents).
- **Pluggable Tool-Agnostic Providers (`igprompts/providers.py`)**:
  - `ManualProvider`: File-based handoff for any web chat UI, paired with `--resume`.
  - `CommandProvider`: Stdin/stdout pipe to any local CLI via `--cmd` or `IGPROMPTS_LLM_CMD`.
  - `DryRunProvider`: Offline verification with clear `[dry-run]` markers (no invented fake content).
- **7-Day Experiment Ledger & Review Loop (`igprompts/experiments.py`)**:
  - Pairs Prompt 12 (planning) with Prompt 10 (diagnostic rewriting).
  - Generates UTF-8 BOM CSV files (Excel on Windows compatible) and calculates rates/rankings.
  - Automatically exports Markdown reports and formats Prompt 10 inputs.
- **Spec-Driven Headless SVG Renderer (`igprompts/renderer.py`)**:
  - Renders directly from explicit ` ```slides ` blocks; fails loudly if no spec is supplied.
  - Added `examples/sample_slides.md`.
- **Unit Tests Expanded to 31 Tests**: 100% coverage across core, models, workflow, providers, renderer, experiments, and CLI.
