[English](ROADMAP.en.md) | 中文版

# 自動化工作流演進路線圖 (Workflow Automation Roadmap)

本專案旨在將社群成長體系，演進為一套**工具中立（Model & Agent Agnostic）、純本機、可擴展且具備嚴謹工程治理**的自動化內容生產管線。

不限制使用者使用哪一個 AI 工具：無論你慣用 Claude、ChatGPT、Gemini、DeepSeek、本地 Ollama 還是自建 Agent，所有 Prompt 均為標準化純文字，工作流引擎支援手動交接、命令列管線串接與 Python 函式。

```
[Prompt 知識庫：全局統一編號 01 ~ 12]
       │
       ├─ Series 1: 圖文與不露臉精準留存體系 (Prompts 01 ~ 05)
       └─ Series 2: 短影音爆款與假設驗證體系 (Prompts 06 ~ 12)
       │
       ▼
[Phase 1: 工具中立工作流引擎] ◀── 已實作 (v0.3.0)
  - 狀態機 (pending -> running -> completed | awaiting_response | failed)
  - 檢查點儲存與斷點續跑 (Checkpoint & Resume)
  - 多元 Provider 支援：
    • ManualProvider：輸出 Markdown 檔案，供任何聊天介面複製貼上
    • CommandProvider：以 stdin/stdout 串接任何本機 CLI (如 ollama, llm, claude)
    • CallableProvider：串接自訂 Python 函式或 API
    • DryRunProvider：離線驗證，明確標記 marker，不作假內容
       │
       ▼
[Phase 2: 純本地圖卡與視覺排版引擎] ◀── 已實作 (v0.3.0)
  - 零相依純標準庫 SVG 產生器 (1080x1350 Instagram 4:5 規格)
  - 解析 AI 回覆中的 ```slides 區塊，按規格繪製，無規格時明確認錯
       │
       ▼
[Phase 3: 7 天測試帳本與復盤閉環] ◀── 已實作 (v0.3.0)
  - Prompt 12 排出測試表 -> `experiment plan` 產生 CSV 帳本
  - 創作者填入實際後台數據 -> `experiment report` 計算各項指標與排名
  - 自動生成「可確定的結論」與「數據看不出來的盲點」
  - 一鍵填入 Prompt 10（復盤與重寫），完成成長閉環
       │
       ▼
[Phase 4: 多渠道發布與主題庫批次執行] ◀── 已實作 (v0.4.0)
  - 內容發布日曆引擎 (`igprompts/calendar.py`)
  - 支援 Notion Database、Airtable、Buffer (CSV) 與 Markdown 視覺排程表
  - 主題庫隊列批次處理器 (`igprompts/batch.py`)：支援 JSON / CSV 隊列批量推進
       │
       ▼
[Phase 5: 雲端排程與 Webhook 生態整合] (未來展望)
  - 支援 GitHub Actions Schedule (cron) 自動推進批次隊列
  - 支援 Webhook 觸發（如 Zapier / Make / n8n）與社群發布通知
```

---

## 階段劃分與最新實作狀態

### Phase 1: 工具中立工作流引擎 (已完成 v0.3.0)
- **核心模組**：`igprompts/providers.py`、`igprompts/workflow.py`
- **特點**：
  - 徹底消除特定模型綁定。
  - 支援手動交接模式（`ManualProvider`）：自動在 `handoff/` 產出提示詞與等待回覆檔案，可與任何網頁或 App 協作。
  - 支援命令列管道模式（`CommandProvider`）：透過 `IGPROMPTS_LLM_CMD` 環境變數或 `--cmd` 參數直接管線呼叫任何終端工具。

### Phase 2: 純本地圖卡渲染 (已完成 v0.3.0)
- **核心模組**：`igprompts/renderer.py`
- **特點**：
  - 純 Python 標準庫實現，輸出 1080x1350 向量圖卡。
  - 圖卡內容完全來自 AI 或創作者的真實規格（````slides` 標籤），杜絕假資料。

### Phase 3: 7 天測試帳本與復盤 (已完成 v0.3.0)
- **核心模組**：`igprompts/experiments.py`
- **特點**：
  - 連結 Prompt 12（測試排程）與 Prompt 10（數據診斷與重寫）。
  - CSV 支援 UTF-8 BOM，在 Windows Excel 中開啟不亂碼。
  - 空白數據保留為未測（`—`），絕不擅自填 0，維持實證原則。

### Phase 4: 多渠道發布與主題庫批次執行 (已完成 v0.4.0)
- **核心模組**：`igprompts/calendar.py`、`igprompts/batch.py`
- **特點**：
  - **多渠道發布日曆**：可由 7 天測試帳本（Prompt 12）或工作流狀態直接衍生發布日曆，支援匯出 Notion Database、Airtable Content Calendar、Buffer 排程 CSV 及 Markdown 表格。
  - **主題庫批次推進**：可讀取 JSON 或 CSV 主題清單（`examples/sample_topics_queue.json`、`sample_topics_queue.csv`），依所屬系列自動批次執行管線並分別留存檢查點與清單。

### Phase 5: 雲端排程與 Webhook 整合 (未來展望)
- 支援 GitHub Actions Schedule (cron) 定時推進隊列。
- 支援與 Zapier / Make / n8n 等自動化中樞透過 Webhook 串接。
