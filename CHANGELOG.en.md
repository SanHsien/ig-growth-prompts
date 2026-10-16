English | [中文版](CHANGELOG.md)

# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 2026-10-17

### Added

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
