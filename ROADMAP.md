[English](ROADMAP.en.md) | 中文版

# 自動化工作流演進路線圖 (Workflow Automation Roadmap)

本專案旨在將社群爆款與不露臉 Prompt 體系，進一步演進為一套**純本機、可擴展、可插拔、具備工程治理**的自動化內容生產管線。

```
[原始 Prompts 框架]
       │
       ▼
[Phase 1: 工作流狀態機與執行器]  ◀── 本次實作核心
  - Step-by-step 狀態機 (pending -> running -> completed)
  - 檢查點儲存與斷點續跑 (Checkpoint & Resume)
  - 可插拔 Provider 介面 (DryRun / Interactive / LLM Protocol)
       │
       ▼
[Phase 2: 純本地視覺/圖卡渲染引擎] ◀── 本次實作核心
  - 零相依純標準庫 SVG 產生器 (1080x1350 IG 4:5 規格)
  - 輪播封面、正文頁與 CTA 導流頁排版
       │
       ▼
[Phase 3: 批次生成與排程隊列]
  - 主題庫 (Topic Pool / Queue) 批次讀取
  - 內容日曆排程自動規劃 (Content Calendar Scheduler)
       │
       ▼
[Phase 4: 多渠道發布與生態整合]
  - 匯出符合 Buffer / Notion / Airtable 的發布清單
  - GitHub Actions 定時執行與 Issue/PR 驅動生產
```

---

## 階段劃分與詳細規劃

### Phase 1: 結構化工作流引擎與狀態流轉 (已實作)
- **目標**：讓 5 步內容生產從「單純複製文字」升級為「具備狀態控制的工程化 Pipeline」。
- **交付物**：
  - `igprompts/workflow.py`：
    - `WorkflowState`：記錄執行階段、輸入變數、各步產出與時間戳記。
    - `StepRunner`：負責依序或指定步驟執行，支援單步重試。
    - `WorkflowProvider`：抽象執行層，預設提供免連網的 `DryRunProvider` 及人機互動 `InteractiveProvider`，相容任意自訂函式或 LLM API。
    - 支援保存 `checkpoint.json` 與斷點續跑（`--resume`）。

### Phase 2: 純本地圖卡與視覺渲染引擎 (已實作)
- **目標**：解決不露臉內容（輪播貼文）排版繁瑣的問題，達成零外部依賴、純本地一鍵產生可發布視覺素材。
- **交付物**：
  - `igprompts/renderer.py`：
    - 原生生成向量 SVG 格式（1080x1350，Instagram 4:5 直式標準尺寸）。
    - 支援深色模式、大標題、文字自動換行排版、分頁指示器與結尾 CTA 視覺導流。
    - CLI 指令 `render-slides` 與 Pipeline 整合，自動輸出至 `slides/` 目錄。

### Phase 3: 主題庫批次排程與內容日曆 (下一步規劃)
- **目標**：支援大量選題的批次產出與發布時間分配。
- **規劃項目**：
  - `topics.json` 批次隊列解析。
  - 自動產生每週／每月貼文排程表（Markdown 內容日曆）。
  - 留存與發布狀態追蹤器。

### Phase 4: 多平台整合與 Webhook 生態 (未來展望)
- **目標**：無縫串接外部社群管理與筆記工具。
- **規劃項目**：
  - Notion Database / Airtable 匯出結構。
  - Webhook 觸發器與 GitHub Actions 排程定時發布草稿。
