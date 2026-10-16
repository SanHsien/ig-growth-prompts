[English](CHANGELOG.en.md) | 中文版

# 變更紀錄

格式參考 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.1.0/)，新的在上面。

## 2026-10-17

### 新增

- **自動化工作流引擎（Phase 1）**：
  - `igprompts/workflow.py`：實現 `WorkflowState`、`StepRunner`、`DryRunProvider`、`CallableProvider`。
  - 支援步驟級狀態流轉（pending、running、completed、failed）、檢查點保存（`save_checkpoint`）與斷點續跑（`--resume`）。
  - 自動生成執行清單 `pipeline_manifest.md` 與狀態檔案 `workflow_state.json`。
- **純本地向量 SVG 輪播圖產生器（Phase 2）**：
  - `igprompts/renderer.py`：零第三方依賴，純標準庫生成 1080x1350（Instagram 4:5 直式標準比例）的高質感深色主題輪播卡（封面、內頁、CTA 導流頁）。
- **CLI 擴展**：
  - 新增 `python -m igprompts run-pipeline`：一鍵執行 5 階段工作流並可帶 `--render-slides` 同步產出視覺圖卡。
  - 新增 `python -m igprompts render-slides`：直接從 state 或設定檔產出完整輪播圖卡集。
- **路線圖規劃**：新增雙語路線圖文件 `ROADMAP.md` 與 `ROADMAP.en.md`。
- **單元測試擴充**：新增 `tests/test_workflow.py` 與 `tests/test_renderer.py`，總測試數增加至 24 個且全數通過。

- `igprompts` 核心套件（純 Python 內建標準函式庫 stdlib-only，零第三方依賴）：
  - 支援 5 大 Prompt 規格檢索、變數解析、單一 Prompt 渲染與缺漏警示。
  - 支援 `pipeline` 指令生成 5 階段完整內容生產線 Markdown 文件。
- CLI 命令列介面：
  - `python -m igprompts list`：列出所有 Prompt、Key 與所需輸入變數。
  - `python -m igprompts show <id>`：檢視指定 Prompt 原型範本。
  - `python -m igprompts render <id> [--json-file] [--var key=value]`：注入變數生成即用 Prompt。
  - `python -m igprompts pipeline [--json-file] [-o output.md]`：一鍵匯出全流水線。
- 示範設定：`examples/sample_inputs.json`（展示 AI 與軟體架構實戰的參數範例）。
- 品質閘門與工具：
  - `tools/dev_check.ps1`：Windows 原生品質檢測工具（單元測試、Markdown 相對連結、Git 空白與換行檢查）。
  - `tools/check_links.py`：純本地 Markdown 相對連結與錨點檢查器。
  - `.github/workflows/ci.yml`：跨平台 GitHub Actions CI（Windows PowerShell 驗證 + Ubuntu Python 3.10 / 3.13 矩陣測試）。
- 完整治理規格與雙語文件：
  - `AGENTS.md`：AI 協作單一真相源規範。
  - `CLAUDE.md`：Claude 專屬提示與驗證指引。
  - `README.md` 與 `README.en.md`：完整中英雙語專案說明。
  - `CHANGELOG.md` 與 `CHANGELOG.en.md`：中英雙語變更歷程。
  - `LICENSE`：MIT 授權條款。
  - `.editorconfig` 與 `.gitattributes`：確保全儲存庫換行（LF）與 UTF-8 編碼一致性。
- 自動化單元測試：
  - `tests/test_prompts.py` 與 `tests/test_cli.py` 共 15 個測試案例，覆蓋率 100%。
