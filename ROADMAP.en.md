English | [中文版](ROADMAP.md)

# Workflow Automation Roadmap

This document outlines the systematic evolution from raw prompts into an automated, extensible, and locally verifiable content production pipeline.

```
[Raw Prompt Framework]
       │
       ▼
[Phase 1: Workflow State Machine & Runner]  ◀── Implemented in this iteration
  - Step-by-step state machine (pending -> running -> completed)
  - Checkpoint persistence & resumption
  - Pluggable provider interface (DryRun / Interactive / LLM Protocol)
       │
       ▼
[Phase 2: Local Headless Visual & Card Renderer] ◀── Implemented in this iteration
  - Zero-dependency standard library SVG card generator (1080x1350 4:5 aspect ratio)
  - Dark mode carousel slides (Cover, Body, and Call-To-Action)
       │
       ▼
[Phase 3: Batch Queue & Content Calendar Scheduling]
  - Batch parsing of topic queues
  - Automated weekly/monthly content calendar generation
       │
       ▼
[Phase 4: Multi-Channel Publishing & Ecosystem Integrations]
  - Export structures for Notion, Airtable, and Buffer
  - Scheduled generation via GitHub Actions and webhooks
```

---

## Detailed Roadmap Phases

### Phase 1: Structured Workflow Engine & State Machine (Completed)
- **Objective**: Upgrade 5-step content generation from static text pasting to a managed stateful pipeline.
- **Deliverables**:
  - `igprompts/workflow.py`:
    - `WorkflowState`: Tracks pipeline stages, input parameters, step outputs, and execution timestamps.
    - `WorkflowRunner`: Orchestrates step sequencing with retry and resumption capabilities.
    - `WorkflowProvider`: Pluggable execution contract. Comes built-in with an offline `DryRunProvider` and CLI `InteractiveProvider`, with an open contract for custom LLM backends.
    - Checkpoint persistence and `--resume` support.

### Phase 2: Local Headless Visual & Card Renderer (Completed)
- **Objective**: Automate the creation of faceless visual carousels with zero external dependencies.
- **Deliverables**:
  - `igprompts/renderer.py`:
    - Native SVG vector generation (1080x1350 resolution for Instagram 4:5 vertical standards).
    - Dark mode styling, auto-wrapped typography, slide pagination dots, and CTA cards.
    - Seamless CLI integration via `render-slides` and `run-pipeline --output-dir`.

### Phase 3: Batch Queue & Content Calendar (Next Milestone)
- **Objective**: Support bulk content production across topic queues.
- **Planned Scope**:
  - `topics.json` batch queue processor.
  - Automated generation of weekly and monthly content calendars in Markdown and JSON.

### Phase 4: Multi-Channel Integrations & Ecosystem (Future Scope)
- **Objective**: Direct interoperability with scheduling tools and databases.
- **Planned Scope**:
  - Notion Database and Airtable synchronization exports.
  - Webhook endpoints and GitHub Actions automated generation.
