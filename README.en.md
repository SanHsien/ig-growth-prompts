English | [中文版](README.md)

# Instagram Growth & Faceless Content Prompt Framework (IG Growth Prompts)

This repository curates and systematically deconstructs the "Claude IG Prompt Series" originally shared by creator `@jasonxtsai`. The underlying workflow helped scale an Instagram account from 0 to 60k followers and 8M views in two months. Here, it is abstracted into 5 standardized, plug-and-play prompt modules, accompanied by a zero-dependency (Python standard library only) CLI tool to help creators and engineers rapidly produce personalized, high-performing post scripts.

---

## Key Features

- **Zero Third-Party Dependencies**: The `igprompts` core tool runs entirely on the Python standard library (`stdlib-only`). No `pip install` required.
- **5 Structured Prompt Modules**: Covers anti-cliché topic discovery, 15 hooks across 5 distinct psychology angles, 3 faceless content variants, retention/completion rate rewriting, and authoritative low-profile positioning.
- **End-to-End Production Pipeline (SOP)**: Generate the complete 5-stage content creation pipeline with a single CLI command.
- **Strict Engineering Standards**: Includes a native Windows quality check gate (`tools/dev_check.ps1`), offline Markdown link validation, bilingual documentation, and GitHub Actions CI.

---

## Repository Structure

```
ig-growth-prompts/
├── .github/workflows/ci.yml            # Cross-platform CI pipeline (Windows + Ubuntu)
├── .editorconfig                       # Indentation & encoding rules (UTF-8, LF)
├── .gitattributes                      # Git line ending normalization (eol=lf)
├── .gitignore                          # Python / IDE ignore rules
├── AGENTS.md                           # AI Agent governance (Single Source of Truth)
├── CLAUDE.md                           # Claude-specific guidance & testing protocol
├── CHANGELOG.md                        # Traditional Chinese Changelog (Keep a Changelog)
├── CHANGELOG.en.md                     # English Changelog
├── LICENSE                             # MIT License
├── README.md                           # Traditional Chinese documentation
├── README.en.md                        # English documentation
├── igprompts/                          # Core Python package (stdlib-only)
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py                          # CLI implementation
│   ├── core.py                         # Template retrieval and variable rendering
│   └── models.py                       # Prompt definitions & metadata
├── prompts/                            # 5 core prompt specifications and transcripts
│   ├── 01-niche-ideation.md            # Prompt 1: Niche Ideation & Anti-cliché Strategy
│   ├── 02-hook-generator.md            # Prompt 2: 15 Hooks across 5 Core Archetypes
│   ├── 03-faceless-formats.md          # Prompt 3: 3 Faceless High-reach Formats
│   ├── 04-retention-optimization.md    # Prompt 4: Retention, Read-through & Saves
│   └── 05-authority-positioning.md     # Prompt 5: Low-Profile Authority Positioning
├── workflow/
│   └── content_pipeline.md             # 5-stage content pipeline SOP
├── examples/
│   └── sample_inputs.json              # Sample configuration payload
├── tests/                              # Unit test suite
│   ├── test_cli.py
│   └── test_prompts.py
└── tools/                              # Quality gate & maintenance tools
    ├── check_links.py                  # Offline Markdown relative link resolver
    └── dev_check.ps1                   # Windows-native Canonical Quality Gate
```

---

## CLI Quickstart

### 1. List Available Prompts and Required Variables
```bash
python -m igprompts list
```
Sample output:
```text
ID   Key                      Title                          Required Variables
------------------------------------------------------------------------------------------
1    niche_ideation           利基市場防套路與原創點子       niche, audience, goal
2    hook_generator           15 句 5 種類型開場 Hook 生成器 idea, audience, tone
3    faceless_formats         3 種不露臉高觸及內容改造       idea, audience, goal
4    retention_optimization   留存率、完讀率與互動指標優化   content, voice, audience
5    authority_positioning    不吹噓的個人品牌專業權威改寫   content, audience, brand_voice
```

### 2. View Raw Prompt Templates
```bash
python -m igprompts show 1
```

### 3. Render a Tailored Prompt
Supply variables via CLI arguments or feed a JSON configuration file:
```bash
# Render Prompt 1 via CLI flags
python -m igprompts render 1 \
  --var niche="AI Software Architecture" \
  --var audience="Senior Engineers & Tech Leads" \
  --var goal="Establish Technical Authority & Advisory Funnel"

# Or render from a JSON configuration file
python -m igprompts render 1 --json-file examples/sample_inputs.json
```

### 4. Export the End-to-End Pipeline
```bash
python -m igprompts pipeline --json-file examples/sample_inputs.json -o pipeline_output.md
```

---

## Core Prompts Overview

| # | Role & Focus | Persona / Authority | Mission | Detailed Spec |
|:---|:---|:---|:---|:---|
| **1** | **Anti-Cliché Ideation** | 10-year Growth Consultant (scaled 50 accounts to 100k) | Identify 7 overused clichés; generate 10 anti-cliché original concepts; rank Top 3 | [01-niche-ideation.md](prompts/01-niche-ideation.md) |
| **2** | **Hook Generator** | Viral Copywriter (+40% completion rate) | Output 15 hooks (suspense, counter-intuitive, emotional, data, insider; 3 each); max 15 chars; rank Top 5 | [02-hook-generator.md](prompts/02-hook-generator.md) |
| **3** | **Faceless Formats** | Faceless Content Strategist | Adapt one idea into Carousel, Subtitle-only Reel, and Silent Visual; provide slide/scene text & styling | [03-faceless-formats.md](prompts/03-faceless-formats.md) |
| **4** | **Retention Polish** | Retention Optimization Consultant | Strip weak phrases/fluff; build line-by-line momentum; maximize dwell time, completion, saves & shares | [04-retention-optimization.md](prompts/04-retention-optimization.md) |
| **5** | **Authority Positioning** | Personal Brand Positioning Consultant | Eliminate guru fluff and boastful metrics; produce Textured, Punchy, and Premium versions | [05-authority-positioning.md](prompts/05-authority-positioning.md) |

For complete end-to-end SOP guidelines, see [workflow/content_pipeline.md](workflow/content_pipeline.md).

---

## Notable Prompt Engineering Insights

1. **Negative Constraint First**: Prompts typically ask "give me 10 ideas," resulting in generic outputs. Prompt 1 forces the model to articulate 7 overused tropes first, constructing an effective filter boundary that elevates originality.
2. **Categorical Taxonomy**: Prompt 2 divides hooks into 5 psychological categories, granting creators balanced A/B testing vectors rather than repetitive phrasing.
3. **Anti-AI & Anti-Guru Guardrails**: Explicitly rules out preachy tones, excessive metric-flaunting, and boilerplate robotic phrasing, addressing key failure modes of modern LLM copy.
4. **Production-Ready Deliverables**: Prompts demand scene-by-scene scripts, visual advice (typography/palettes), captions, and CTAs ready to drop into Canva, CapCut, or schedulers.

---

## Local Development & Quality Gates

All modifications must pass the Windows Canonical Quality Gate:

```powershell
pwsh -File tools/dev_check.ps1
```

Validation includes:
1. **Unit tests**: `python -m unittest discover -s tests -p "test_*.py" -v`
2. **Markdown links**: `python tools/check_links.py` (offline verification of all Markdown links and images)
3. **Git whitespace & newline checks**: `git diff --check`

---

## License & Acknowledgments

- Original Concepts & Prompts: `@jasonxtsai` (Instagram)
- Architecture, CLI Tooling & Engineering Governance: [SanHsien](https://github.com/SanHsien)
- License: [MIT License](LICENSE)
