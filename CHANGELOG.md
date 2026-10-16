[English](CHANGELOG.en.md) | 中文版

# 變更紀錄

格式參考 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.1.0/)，新的在上面。

## [0.4.0] - 2026-10-17

### 新增

- **Phase 4 多渠道內容發布日曆引擎 (`igprompts/calendar.py`)**：
  - 支援將 7 天測試帳本（Prompt 12）或完成的工作流狀態轉換為發布日曆項目。
  - 支援四種匯出格式：Notion Database (CSV, UTF-8 BOM)、Airtable Content Calendar (CSV, UTF-8 BOM)、Buffer 社群排程器 (CSV) 以及 Markdown 視覺發布日曆表格。
- **Phase 4 主題庫批次執行模組 (`igprompts/batch.py`)**：
  - 支援載入 JSON 或 CSV 主題隊列清單（提供範例 `examples/sample_topics_queue.json` 與 `sample_topics_queue.csv`）。
  - 自動依主題指定之 series 循序執行管線，為每個主題獨立建立目錄、檢查點與 Markdown 清單。
- **CLI 擴展**：
  - 新增 `python -m igprompts calendar generate` 命令，支援 `--from-ledger`、`--from-state`、`--format` 與 `--output`。
  - 新增 `python -m igprompts batch run` 命令，支援 `-f/--queue`、`--provider` 與 `--output-dir`。
- **單元測試擴增至 43 個**：新增 `test_calendar.py` 與 `test_batch.py`，完整覆蓋日曆匯出與批次隊列邏輯。

## [0.3.0] - 2026-10-17

### 新增

- **Reels 短影音爆款與假設驗證體系（全庫 Prompts 06 ~ 12）**：
  - 收錄全部 7 組短影音 Prompt：`06-reels-7day-topics.md` ~ `12-reels-seven-day-test-matrix.md`。
  - 涵蓋 7 天選題、1~3 秒 Hook、完播分鏡腳本、轉發動機、數據診斷、策略跟風與 7 天測試表。
- **全庫統一編號與 AI 工具中立化（Model & Agent Agnostic）**：
  - 全局統一編號 01 ~ 12，消除先前兩個系列同時從 01 開始的命名混淆問題。
  - 移除特定廠商/模型名稱鎖定（將命名正規化為 `faceless_carousel` 與 `short_video_reels`）。
  - 明確支援任何使用者屬意的 AI 工具（ChatGPT, Claude, Gemini, DeepSeek, Ollama, 自建 Agent）。
- **工具中立 Provider 架構（`igprompts/providers.py`）**：
  - `ManualProvider`：以檔案交接方式支援任何 Web 聊天介面，支援 `--resume` 斷點續跑。
  - `CommandProvider`：透過 stdin/stdout 串接任何終端 CLI（支援 `--cmd` 或 `IGPROMPTS_LLM_CMD`）。
  - `DryRunProvider`：離線驗證，明確標記 `[dry-run]`，絕不捏造假內容。
- **7 天測試帳本與復盤模組（`igprompts/experiments.py`）**：
  - 串聯 Prompt 12（排表）與 Prompt 10（復盤與重寫）。
  - 支援 CSV 生成與解析（UTF-8 BOM 相容 Windows Excel），自動計算各項互動率與排名。
  - 自動生成 Markdown 分析報告，並可一鍵填寫 Prompt 10 輸入。
- **純真實規格的 SVG 輪播圖產生器（`igprompts/renderer.py`）**：
  - 移除先前的死程式碼假資料，改為嚴格解析 ` ```slides ` 規格區塊。
  - 提供 `examples/sample_slides.md` 範例檔。
- **單元測試增至 31 個**：覆蓋 core、models、workflow、providers、renderer、experiments 與 CLI 全指令。
