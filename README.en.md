<div align="center">
  <h1>🎯 Instagram Growth & Faceless Content Prompt Framework</h1>
  <p><strong>Full-Lifecycle IG Algorithmic Growth Prompts & Automation Toolkit (Unified 01-12, Python Stdlib Workflow, Standalone GUI, Calendar & Batch Runner)</strong></p>

  <p>
    <a href="https://github.com/SanHsien/ig-growth-prompts/releases">
      <img src="https://img.shields.io/github/v/release/SanHsien/ig-growth-prompts?color=blue&style=flat-square" alt="GitHub Release">
    </a>
    <a href="https://github.com/SanHsien/ig-growth-prompts">
      <img src="https://img.shields.io/badge/Version-0.6.1-blue?style=flat-square" alt="Version">
    </a>
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
    <img src="https://img.shields.io/badge/Dependencies-Zero%20(stdlib--only)-success?style=flat-square" alt="Zero Dependencies">
    <a href="https://github.com/SanHsien/ig-growth-prompts/actions/workflows/ci.yml">
      <img src="https://img.shields.io/github/actions/workflow/status/SanHsien/ig-growth-prompts/ci.yml?branch=main&label=CI&style=flat-square" alt="CI Status">
    </a>
    <a href="https://github.com/SanHsien/ig-growth-prompts/actions/workflows/codeql.yml">
      <img src="https://img.shields.io/github/actions/workflow/status/SanHsien/ig-growth-prompts/codeql.yml?branch=main&label=CodeQL&style=flat-square" alt="CodeQL Status">
    </a>
    <a href="./LICENSE">
      <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
    </a>
  </p>

  <p>
    <a href="#key-features">Features</a> •
    <a href="#prompts-overview-unified-ids-01--12">Prompts (01-12)</a> •
    <a href="#cli-quickstart">CLI Quickstart</a> •
    <a href="./ROADMAP.en.md">Roadmap</a> •
    <a href="./SECURITY.md">Security</a> •
    <a href="./REVIEW.md">Review</a>
  </p>

  <p>
    <a href="./README.md">繁體中文</a> |
    <strong>English</strong>
  </p>
</div>

---

This repository curates and systematically deconstructs the Instagram growth systems originally shared by creator `@jasonxtsai` (covering both faceless carousels and short-form video reels). Here, it is abstracted into **12 structured prompt modules with unified IDs (01 ~ 12)**, accompanied by a zero-dependency (Python standard library only) workflow engine, desktop GUI, multi-platform publishing calendar exporter, batch queue runner, experiment ledger, and SVG carousel card renderer.

> [!IMPORTANT]
> **Model & Agent Agnostic**
> All prompts and tooling in this repository are strictly tool-agnostic. You are never locked into a specific vendor or agent. Feel free to use your preferred AI tools: web chats (Claude, ChatGPT, Gemini, DeepSeek, v0), local models (Ollama, LLaMA), CLI commands (`llm`, `claude -p`), or custom AI coding agents.

---

## Key Features

- **Zero Third-Party Dependencies**: The `igprompts` core tool runs entirely on the Python standard library (`stdlib-only`). No `pip install` required.
- **Standalone Portable & Setup Installer GUI**: Full desktop GUI built with Tkinter, supporting Light, Dark, and Native Windows system theme switching.
- **Batch Queue & Scheduled Runner**: Run series in sequence or parallel, with support for local background scheduling and GitHub Actions cron automation.
- **Multi-Platform Publishing Calendar**: Export manifests to Markdown, Notion CSV, Airtable CSV, and Buffer-ready schedules.
- **12 Structured Prompt Modules with Unified IDs**:
  - **Series 1 (01 ~ 05)**: Faceless & Carousel System (anti-cliché ideation, 15-char hooks, faceless adaptation, greased-chute copy, low-profile authority).
  - **Series 2 (06 ~ 12)**: Short-Form Video & Reels System (7-day topics, 1-3s hooks, retention scripts, viral sharing, data diagnosis, strategic trend jacking, 7-day test matrix).
- **Pluggable Execution Providers**:
  - `manual`: File-based handoff in `handoff/` for copy-pasting to any chat UI, paired with `--resume`.
  - `command`: Stream prompts directly to local CLIs via standard input/output (stdin/stdout).
  - `dry-run`: Deterministic offline verification with explicit markers (no invented fake content).
- **Headless Vector SVG Carousel Generator**: Pure Python stdlib generator producing 1080x1350 (Instagram 4:5 vertical) dark-mode vector cards.
- **7-Day Experiment Ledger & Review Loop**: Prompt 12 generates the plan -> CSV ledger records actual stats -> automated metric calculation -> feeds directly into Prompt 10 for diagnostic rewriting.
- **Clear Evolution Roadmap & Review**: Documented in [ROADMAP.en.md](ROADMAP.en.md) and [REVIEW.md](REVIEW.md).


---

## Prompts Overview (Unified IDs 01 ~ 12)

### Series 1: Faceless & Carousel System (Prompts 01 ~ 05)

| ID | Focus | Persona / Authority | Mission | Detailed Spec |
|:---|:---|:---|:---|:---|
| **01** | **Anti-Cliché Ideation** | 10-year Growth Consultant (scaled 50 accounts) | Identify 7 overused clichés; generate 10 anti-cliché concepts; rank Top 3 | [01-niche-ideation.md](prompts/01-niche-ideation.md) |
| **02** | **Hook Generator** | Viral Copywriter (+40% completion rate) | Output 15 hooks (suspense, counter-intuitive, emotional, data, insider); max 15 chars | [02-hook-generator.md](prompts/02-hook-generator.md) |
| **03** | **Faceless Formats** | Faceless Content Strategist | Adapt one idea into Carousel, Subtitle Reel, and Silent Visual with full specs | [03-faceless-formats.md](prompts/03-faceless-formats.md) |
| **04** | **Retention Polish** | Retention Optimization Consultant | Strip weak phrases/fluff; build line-by-line momentum; maximize dwell & saves | [04-retention-optimization.md](prompts/04-retention-optimization.md) |
| **05** | **Authority Positioning** | Personal Brand Positioning Consultant | Eliminate guru fluff and boastful metrics; produce Textured, Punchy, Premium versions | [05-authority-positioning.md](prompts/05-authority-positioning.md) |

### Series 2: Short-Form Video & Reels System (Prompts 06 ~ 12)

| ID | Focus | Persona / Authority | Mission | Detailed Spec |
|:---|:---|:---|:---|:---|
| **06** | **7-Day Topics** | Reels Strategy Consultant | Anchor to follower count and stage goals; produce 7 viable topic concepts | [06-reels-7day-topics.md](prompts/06-reels-7day-topics.md) |
| **07** | **Top Opening Hooks** | Viral Short-Form Copywriter | Output 20 hooks across 8 psychological mechanisms; rank Top 5 | [07-reels-top-hooks.md](prompts/07-reels-top-hooks.md) |
| **08** | **Retention Scripts** | Video Retention Director | 7 key components: hook, storyboard, voiceover, on-screen text, pacing, seconds | [08-reels-retention-script.md](prompts/08-reels-retention-script.md) |
| **09** | **Save & Share** | Viral Growth Consultant | 5 angles (practical, identity, emotional, surprise, problem); altruistic sharing | [09-reels-save-and-share.md](prompts/09-reels-save-and-share.md) |
| **10** | **Video Revival** | Video Data Analyst | Separate confirmed insights from speculative guesses; diagnose & rewrite | [10-reels-revival.md](prompts/10-reels-revival.md) |
| **11** | **Strategic Trends** | Trend Strategy Analyst | "Mechanism != Video": abstract viral mechanics to niche; flag saturation | [11-reels-strategic-trends.md](prompts/11-reels-strategic-trends.md) |
| **12** | **Testing Matrix** | Experiment Scheduling Consultant | 7-day orthogonal variance testing matrix with explicit hypotheses & metrics | [12-reels-seven-day-test-matrix.md](prompts/12-reels-seven-day-test-matrix.md) |

---

## CLI Quickstart

### 1. List and Render Prompts
```bash
# List all 12 prompts
python -m igprompts list

# Filter short-form reels series (Prompts 06-12)
python -m igprompts list --series reels

# Inspect a raw template
python -m igprompts show 06

# Render a prompt with variables (ready to paste into any AI chat)
python -m igprompts render 06 --json-file examples/sample_inputs.json
```

### 2. Manual Handoff Mode (Works with any Chat UI)
```bash
python -m igprompts run-pipeline \
  --series faceless \
  --json-file examples/sample_inputs.json \
  --provider manual \
  -o my_work
```
1. Paste `my_work/handoff/01-niche_ideation.prompt.md` into your AI chat tool.
2. Save the answer as `01-niche_ideation.response.md`.
3. Re-run `python -m igprompts run-pipeline --resume --provider manual -o my_work` to proceed to the next step.

### 3. Command Pipe Mode (Local LLM / CLI)
```bash
python -m igprompts run-pipeline \
  --series faceless \
  --json-file examples/sample_inputs.json \
  --provider command \
  --cmd "ollama run llama3" \
  -o my_work
```

### 4. 7-Day Experiment Ledger & Review Loop (Phase 3)
```bash
# Step A: Initialize CSV ledger based on Prompt 12
python -m igprompts experiment plan --csv ledger.csv

# Step B: Record real view/save/share numbers from the Instagram dashboard

# Step C: Generate analysis report and feed directly into Prompt 10
python -m igprompts experiment report \
  --csv ledger.csv \
  --output report.md \
  --prompt-out prompt10_input.txt
```

### 5. Headless 1080x1350 Carousel SVG Generation
```bash
python -m igprompts render-slides --from examples/sample_slides.md -o slides_out
```

### 6. Multi-Channel Content Calendar (Phase 4)
Convert 7-day experiment ledgers or workflow checkpoints into ready-to-publish schedules with exporters for Notion, Airtable, Buffer, and Markdown:
```bash
# Export all channels from experiment ledger
python -m igprompts calendar generate \
  --from-ledger ledger.csv \
  --start-date 2026-11-01 \
  --format all \
  -o calendar_export

# Export Notion CSV only
python -m igprompts calendar generate \
  --from-ledger ledger.csv \
  --format notion \
  -o notion.csv

# Aggregate all batch outputs into a single staggered content calendar
python -m igprompts calendar generate \
  --from-batch batch_output \
  --interval 2 \
  --format all \
  -o calendar_export
```

### 7. Batch Topic Queue Runner (Phase 4)
Queue multiple topics in JSON or CSV and run workflows sequentially:
```bash
python -m igprompts batch run \
  -f examples/sample_topics_queue.json \
  --provider dry-run \
  -o batch_output
```

### 8. GitHub Actions Scheduled Automation (Phase 5)
Repository includes [Scheduled Batch Topic Runner](.github/workflows/batch_schedule.yml):
- **Cron Schedule**: Runs automatically every day at 02:00 UTC (10:00 AM UTC+8) to process queues and build calendars.
- **Manual Trigger**: Supports `workflow_dispatch` with custom queue files (JSON / CSV), provider selection, and calendar options.
- **Artifacts & Summary**: Publishes visual Markdown calendars directly to `$GITHUB_STEP_SUMMARY` and uploads full output packages (SVG slides, CSV schedules, manifests) as job artifacts.

### 9. Standalone Desktop GUI Workbench (Phase 6)
Zero-dependency visual application with instant live log, calendar export, and theme switcher:
```bash
# Launch GUI from CLI
python -m igprompts gui
# Or run one-click setup script
pwsh -File install.ps1
```
- **Three Themes**: "🌙 Dark", "☀️ Light", and "💻 System Default" (natively detects Windows 11 `AppsUseLightTheme` registry).
- **Execution Flexibility**: Check Series 1 (Faceless), Series 2 (Reels), or run both concurrently.
- **Local Scheduler**: Tab generates Windows Task Scheduler batch scripts (`.bat`) for automated local runs.

### 10. Portable Binary & Windows Setup Installer (SemVer)
Dual distribution packages built with Semantic Versioning:
- **Portable Standalone Executable**: `dist/igprompts-gui-v0.6.1-portable.exe` (run anywhere, no Python required)
- **Windows Setup Installer**: `dist/igprompts-setup-v0.6.1.exe` (Inno Setup with desktop icons and start menu items)
- **Local Compiler**:
  ```powershell
  pwsh -File tools/build_exe.ps1
  ```
- **Cloud Packaging Pipeline**: [Build and Release Windows GUI](.github/workflows/release_gui.yml) automatically builds and publishes release assets on version tags.

---

## Local Development & Quality Gates

All modifications must pass the Windows Canonical Quality Gate:

```powershell
pwsh -File tools/dev_check.ps1
```

Verification includes 49 unit tests, full Markdown link validation, and git diff whitespace hygiene.

---

## Private Repository CodeQL Template (CI Template)

When setting up CodeQL security analysis on private GitHub repositories:
- **Template File**: [`tools/ci-templates/codeql-private.yml`](tools/ci-templates/codeql-private.yml)
- **Context & Pain Point**: GitHub Private Repositories require a paid GitHub Advanced Security (GHAS) license to upload SARIF results to the GitHub Code Scanning API. Standard CodeQL workflows will fail with `Code scanning is not enabled for this repository` without GHAS.
- **Solution & Design**:
  1. Keeps full static analysis active (`queries: security-extended`) — **0% stripped or degraded security checks**.
  2. Sets `upload: false` during analysis to avoid calling unpaid APIs.
  3. Uses `actions/upload-artifact` to archive the complete `python.sarif` report for inspection, keeping CI green.
- **Cross-Repo Reuse**: Whenever setting up CI for any private repo, developers and AI agents can directly copy this template to `.github/workflows/codeql.yml`.

---

## Project Governance & Documentation

- [Changelog (CHANGELOG.md)](CHANGELOG.md) / [English Changelog](CHANGELOG.en.md)
- [Roadmap (ROADMAP.md)](ROADMAP.md) / [English Roadmap](ROADMAP.en.md)
- [Contributing Guide (CONTRIBUTING.md)](CONTRIBUTING.md)
- [Security Policy (SECURITY.md)](SECURITY.md)
- [Agent Guidelines (AGENTS.md)](AGENTS.md) / [Claude Guide (CLAUDE.md)](CLAUDE.md) / [Gemini Guide (GEMINI.md)](GEMINI.md)

---

## License & Acknowledgments

- Original Concepts & Prompts: `@jasonxtsai` (Instagram)
- Architecture, CLI Tooling & Engineering Governance: [SanHsien](https://github.com/SanHsien)
- License: [MIT License](LICENSE)
