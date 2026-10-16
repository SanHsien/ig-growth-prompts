English | [中文版](ROADMAP.md)

# Workflow Automation Roadmap

This repository transforms social media growth strategies into a **tool-agnostic (Model & Agent Agnostic), local-first, extensible, and strictly governed** content production pipeline.

Users are free to use their preferred AI tools (Claude, ChatGPT, Gemini, DeepSeek, local Ollama, Copilot, or custom coding agents). All prompts are standard plain text, and the workflow engine supports file handoffs, CLI command pipes, and Python callables.

```
[Prompt Knowledge Base: Unified IDs 01 ~ 12]
       │
       ├─ Series 1: Faceless & Carousel Series (Prompts 01 ~ 05)
       └─ Series 2: Short-Form Video & Reels Series (Prompts 06 ~ 12)
       │
       ▼
[Phase 1: Tool-Agnostic Workflow Engine] ◀── Implemented (v0.3.0)
  - State machine (pending -> running -> completed | awaiting_response | failed)
  - Checkpoint persistence and resumption
  - Multi-provider support:
    • ManualProvider: Markdown file handoff for any web chat UI
    • CommandProvider: Standard stdin/stdout piping to any CLI (ollama, llm, claude, etc.)
    • CallableProvider: Wrap custom Python SDKs or agents
    • DryRunProvider: Offline verification with explicit markers (no canned outputs)
       │
       ▼
[Phase 2: Local Headless Visual Card Renderer] ◀── Implemented (v0.3.0)
  - Zero-dependency stdlib SVG generator (1080x1350 Instagram 4:5 vertical)
  - Renders from ```slides markdown blocks produced by AI or users
       │
       ▼
[Phase 3: 7-Day Experiment Ledger & Review Loop] ◀── Implemented (v0.3.0)
  - Prompt 12 generates a test plan -> `experiment plan` writes a CSV ledger
  - User fills actual dashboard metrics -> `experiment report` ranks metrics
  - Categorizes confirmed conclusions vs unknown metrics
  - Directly feeds Prompt 10 for diagnostic rewriting
       │
       ▼
[Phase 4: Multi-Channel Publishing & Batch Queue] ◀── Implemented (v0.4.0)
  - Content Calendar Engine (`igprompts/calendar.py`)
  - Exporters for Notion Database, Airtable Content Calendar, Buffer (CSV), and Markdown
  - Batch Queue Processor (`igprompts/batch.py`) for sequential JSON / CSV topic pipelines
       │
       ▼
[Phase 5: Cloud Automation & Webhook Integrations] (Future Scope)
  - Automated queue runs via GitHub Actions cron schedules
  - Dispatch notifications via Webhooks (Zapier, Make, n8n)
```

---

## Detailed Roadmap Phases

### Phase 1: Tool-Agnostic Workflow Engine (Completed v0.3.0)
- **Modules**: `igprompts/providers.py`, `igprompts/workflow.py`
- Eliminates hardcoded model vendor locks.
- Provides `ManualProvider` for copy-paste handoffs with any chat UI, and `CommandProvider` for command-line pipes.

### Phase 2: Local Headless Visual Card Renderer (Completed v0.3.0)
- **Module**: `igprompts/renderer.py`
- Pure Python standard library implementation generating 1080x1350 SVG cards.
- Renders only explicit slide specs (` ```slides ` blocks); fails loudly if missing instead of inventing dummy slides.

### Phase 3: 7-Day Experiment Ledger & Review Loop (Completed v0.3.0)
- **Module**: `igprompts/experiments.py`
- Pairs Prompt 12 (planning) with Prompt 10 (diagnostic rewriting).
- Generates UTF-8 BOM CSV files compatible with Excel on Windows. Missing data remains marked as unknown (`—`).

### Phase 4: Multi-Channel Publishing & Batch Queue (Completed v0.4.0)
- **Modules**: `igprompts/calendar.py`, `igprompts/batch.py`
- **Content Calendar**: Translates 7-day experiment ledgers or completed workflow states into scheduled calendar items, exporting Notion Database CSV, Airtable Content Calendar CSV, Buffer scheduler CSV, and formatted Markdown tables.
- **Batch Processing**: Reads topic queues from JSON or CSV (`examples/sample_topics_queue.json`, `sample_topics_queue.csv`) and sequentially processes them across series pipelines.

### Phase 5: Cloud Automation & Webhooks (Future Scope)
- GitHub Actions Scheduled (cron) runner for queue execution.
- Webhook endpoints for Zapier / Make / n8n triggers.
