English | [中文版](CHANGELOG.md)

# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.5.0] - 2026-10-17

### Added

- **Phase 5 Scheduled Batch Automation via GitHub Actions (`.github/workflows/batch_schedule.yml`)**:
  - Automatically runs topic queues on a daily cron schedule (`0 2 * * *`).
  - Supports `workflow_dispatch` manual trigger with custom inputs.
  - Generates multi-channel calendar artifacts, posts Markdown summary to `$GITHUB_STEP_SUMMARY`, and uploads job artifacts.
- **Aggregated Batch Calendar Generation (`generate_calendar_from_batch_dir`)**:
  - Scans all `workflow_state.json` checkpoints within a batch run directory and schedules items at custom intervals.
  - Extended CLI support via `calendar generate --from-batch <dir> --interval <days>`.
- **Unit Tests Expanded to 45 Tests**: Added coverage for batch calendar aggregation and CLI integration.

## [0.4.0] - 2026-10-17

### Added

- **Phase 4 Content Calendar Engine (`igprompts/calendar.py`)**:
  - Automatically translates 7-day experiment ledgers or workflow checkpoints into scheduled calendar entries.
  - Multi-channel exporters for Notion Database (CSV, UTF-8 BOM), Airtable Content Calendar (CSV, UTF-8 BOM), Buffer Social Scheduler (CSV), and Markdown visual table calendars.
- **Phase 4 Batch Queue Processor (`igprompts/batch.py`)**:
  - Sequential processing of topic queues from JSON or CSV files (`examples/sample_topics_queue.json`, `sample_topics_queue.csv`).
  - Automatically invokes corresponding series workflows and generates isolated directories, checkpoints, and manifest summaries.
- **CLI Subcommand Extensions**:
  - `python -m igprompts calendar generate`: with options `--from-ledger`, `--from-state`, `--format`, and `--output`.
  - `python -m igprompts batch run`: with options `-f/--queue`, `--provider`, and `--output-dir`.
- **Unit Tests Expanded to 43 Tests**: Added `test_calendar.py` and `test_batch.py` covering calendar exports and batch queues.

## [0.3.0] - 2026-10-17

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
