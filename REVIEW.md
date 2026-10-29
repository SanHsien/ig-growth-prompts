# 證據式代碼審查報告 (Code Review & Verification)

- **審查日期**：2026-10-17
- **審查對象**：`SanHsien/ig-growth-prompts` (v0.6.1)
- **執行環境**：Windows 11 原生（PowerShell 7.5 / Python 3.14.8 / PyInstaller 6.21.0 / Inno Setup 6.4.3 / Git 2.50）
- **審查標準**：比照 `SanHsien/Antigravity-Manager` 生態系之高規格標準架構、純標準庫零外部依賴、防禦性編程與嚴格品質閘門。

---

## 1. 審查結論

**當前狀態：`dev_check.ps1` 全綠燈 PASS，49 個單元測試通過（Ran 49 tests in 0.3s），29 個 Markdown 文件相對鏈結 100% 有效，零未授權第三方 pip 依賴，Windows 免安裝單檔與 Setup 安裝檔皆順利編譯。**

本輪審查與強化涵蓋以下核心項目：
1. **GitHub 治理與安全基建**：比照標準補齊 `.github/CODEOWNERS`、`.github/dependabot.yml`、`.github/PULL_REQUEST_TEMPLATE.md`、`.github/ISSUE_TEMPLATE/`（bug_report、feature_request、config.yml）與 `.github/workflows/codeql.yml` 安全掃描工作流。
2. **安全政策與漏洞通報**：升級 `SECURITY.md`，納入私密漏洞通報連結、零外部依賴供應鏈防護、零遙測離線原則與敏感資訊隔離規範。
3. **門面與說明文件完備性**：重構 `README.md` 與 `README.en.md` 頂部 Header、Badges 徽章（Release、Version、Python 3.10+、License MIT、CI Status、CodeQL、Zero Dependencies）、快速導航錨點與最新專案架構樹狀圖。
4. **GUI 執行緒防禦性修復**：修正 `igprompts/gui.py` 背景線程日誌輸出與按鈕狀態更新邏輯，嚴格改用 `root.after(0, ...)` 派發至 Tkinter 主線程，徹底杜絕跨線程操作 UI 的潛在崩潰風險。
5. **CodeQL 雙模策略與通用範本封存**：評估專案符合公開標準並轉為 Public 後啟用原生 CodeQL 上傳；同時於 `tools/ci-templates/codeql-private.yml` 完整封存私有倉庫專用免 GHAS 授權工作流，供跨專案複用。

---

## 2. 模組代碼審查矩陣 (Code Review Matrix)

| 模組檔案 | 程式碼行數 | 核心職責 | 依賴項 | 審查結果 | 防禦性設計與驗證重點 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `igprompts/models.py` | 347 | 12 組 Prompt 定義與 PromptDefinition 規格 | stdlib (dataclasses) | ✅ 通過 | 唯讀凍結 dataclass (`frozen=True`)，提示詞模板內嵌，不依賴外部檔案讀取，避免單檔 exe 打包後路徑遺失。 |
| `igprompts/core.py` | 107 | 模板檢索、別名正規化、變數渲染引擎 | stdlib (typing) | ✅ 通過 | 支援別名相容（如 `carousel`, `reels`），遺失變數時提供可選佔位符或明確報錯。 |
| `igprompts/providers.py` | 134 | 中立執行提供者 (Manual, Command, DryRun) | stdlib (subprocess, pathlib) | ✅ 通過 | 支援無外部依賴手動交接、本機 CLI pipe 串接與確定性 dry-run 離線驗證。 |
| `igprompts/workflow.py` | 206 | 狀態機、檢查點持久化、Manifest 匯出 | stdlib (json, pathlib) | ✅ 通過 | 每次推進自動建立父目錄，狀態檔採 UTF-8 格式，中途斷點可無損續跑 (`--resume`)。 |
| `igprompts/renderer.py` | 196 | 純本機 SVG 4:5 向量輪播圖卡排版 | stdlib (xml, html, re) | ✅ 通過 | 零依賴純標準庫向量生成，文字自動折行，特殊字元安全轉義，杜絕 XSS 與 XML 語法錯誤。 |
| `igprompts/experiments.py` | 196 | 7 天測試帳本、CSV 讀寫與復盤指標試算 | stdlib (csv, pathlib) | ✅ 通過 | UTF-8-SIG 讀寫，除以零邊界保護（完播率、互動率、轉發率計算），自動串接 Prompt 10。 |
| `igprompts/calendar.py` | 265 | 發布日曆多渠道格式匯出器 | stdlib (csv, datetime) | ✅ 通過 | 匯出 Notion CSV、Airtable CSV、Buffer CSV 與 Markdown，CSV 採用 `utf-8-sig` 防止 Excel 開啟亂碼。 |
| `igprompts/batch.py` | 109 | 佇列排程與批次執行引擎 | stdlib (csv, json) | ✅ 通過 | 支援 JSON 與 CSV 佇列，動態正規化系列名稱，隔離各主題輸出目錄。 |
| `igprompts/gui.py` | 470 | 桌面 Tkinter 工作台 (深/淺/系統三主題) | stdlib (tkinter, winreg) | ✅ 通過 | Windows 11 原生註冊表偵測主題；背景線程非同步運作；`root.after` 安全派發 UI 更新。 |
| `igprompts/cli.py` | 366 | 命令列介面入口與子命令排程 | stdlib (argparse) | ✅ 通過 | 統一入口，支援 10 組子命令 (`list`, `show`, `render`, `pipeline`, `run-pipeline`, `render-slides`, `experiment`, `calendar`, `batch`, `gui`)。 |

---

## 3. 本次審查發現與修復細節 (Findings & Fixes)

### 3.1 Tkinter 跨線程操作防禦性修復 (`igprompts/gui.py`)
- **問題分析**：在 `gui.py` 中，工作流執行是以 `threading.Thread(target=self._run_workflows, daemon=True)` 在背景推進。原先在背景線程中直接呼叫 `self.txt_log.insert()` 與 `self.btn_run.config(state="normal")`，在某些 Windows/Tkinter 環境下可能引發跨執行緒存取 UI 元件的潛在警告或異常。
- **修復方式**：將所有 UI 元件操作改寫為 `append` 與 `restore` 閉包，透過 `self.root.after(0, ...)` 派發回主線程執行，並加入 `winfo_exists()` 與例外保護。
- **驗證方式**：執行 `python -m unittest tests.test_gui` 測試通過，且手動在背景線程派發時日誌安全寫入。

### 3.2 治理規範與 CI 基建補齊
- **問題分析**：原專案缺少 GitHub 標準治理檔案（CODEOWNERS、PR 範本、Issue 範本、Dependabot），且未設定靜態安全掃描工作流。
- **修復方式**：
  - 新增 `.github/CODEOWNERS`，指定維護者 `@SanHsien` 審查責任。
  - 新增 `.github/dependabot.yml`，每週排程自動檢查 GitHub Actions 依賴版本。
  - 新增 `.github/PULL_REQUEST_TEMPLATE.md`，提供繁中自檢與回退指引。
  - 新增 `.github/ISSUE_TEMPLATE/`（`bug_report.md`、`feature_request.md`、`config.yml`），提供結構化表單並引導安全漏洞走私密通道。
  - 新增 `.github/workflows/codeql.yml`，設定每週一與 PR 時自動執行 Python CodeQL 靜態分析。

### 3.3 門面與文件鏈結完備性
- **問題分析**：`README.md` 與 `README.en.md` 缺少頂部徽章群與架構導航，且舊版目錄樹存在歷史殘留項目。
- **修復方式**：更新置中 Header、徽章群（Release、Version、Python、License、CI、CodeQL）、多語導航，並清除過時行號，重新通過 `tools/check_links.py` 檢查。

---

### 3.4 第二輪深度掃描（2026-10-26）

每項皆先寫會失敗的重現測試再修：

- `1044b0b`、`5d1c59e`：批次 manual provider 各主題共用 handoff 目錄；主題 id 重複／含路徑字元（含反斜線、Windows 保留名）
- `16d93ca`：數據表接受 nan／inf
- `77b596f`：`get_prompt("²")` 丟 ValueError
- `6324091`、`9ca68aa`：帶 BOM 的 slide 規格檔與 manual 回覆檔
- `5d97b2c`：Markdown 表格欄位含 `|`／換行；ledger day 為 0、D1 等無效值
- `9a48a6d`：GUI 無設定指令時產生假回答、排程 .bat 路徑未加引號、日曆匯出 ID 重複
- `18405f4`：CSV 匯出未防公式注入（`=HYPERLINK(...)` 等原樣輸出；主管-3 決定加單引號前綴）

### 3.5 檢查點原子寫入（2026-10-29）

- 基準：`fcf111793c1f95806f788c788e4867322bd08bd0`；Windows 11 原生、Python 3.14.10。
- 根因：`WorkflowState.save_checkpoint()` 直接覆寫 JSON，部分寫入失敗會截斷原檔。
- 修正：使用標準庫在同目錄建立唯一暫存檔，寫入後 flush／fsync 並關閉，再以 `Path.replace()` 原子替換；例外向外傳遞，並清理本次暫存檔。
- 先紅：`python -m unittest discover -s tests -p test_workflow.py -v`，exit code 1，`Ran 8 tests`、`FAILED (failures=2)`。部分寫入測試觀察到原檔遭截斷；替換測試為 `OSError not raised`。
- 後綠：相同指令，exit code 0，`Ran 8 tests`、`OK`。兩種失敗均驗證原檔位元組不變、舊狀態可解析、無暫存檔殘留；透過 CLI `--resume` 在含空白路徑下只執行步驟 2–5，保留已完成的步驟 1。
- 完整閘門：`pwsh -File tools/dev_check.ps1`，exit code 0，結尾為 `dev_check: all gates passed`。
- 範圍：驗證本機寫入與替換失敗；不宣稱已驗證斷電耐久性或 GUI 操作。本輪未查詢 GitHub，路線圖的遠端狀態仍為原快照。

## 4. 自動化測試與品質閘門驗證 (Verification Evidence)

執行本機標準化品質閘門：
```powershell
pwsh -File tools/dev_check.ps1
```

**驗證輸出日誌**：
```
==> Unit tests
Ran 49 tests in 0.301s
OK

==> Markdown relative links
OK   .github\ISSUE_TEMPLATE\bug_report.md
OK   .github\ISSUE_TEMPLATE\feature_request.md
OK   .github\PULL_REQUEST_TEMPLATE.md
OK   AGENTS.md
OK   CHANGELOG.en.md
OK   CHANGELOG.md
OK   CLAUDE.md
OK   CONTRIBUTING.md
OK   examples\sample_slides.md
OK   GEMINI.md
OK   prompts\01-niche-ideation.md
OK   prompts\02-hook-generator.md
OK   prompts\03-faceless-formats.md
OK   prompts\04-retention-optimization.md
OK   prompts\05-authority-positioning.md
OK   prompts\06-reels-7day-topics.md
OK   prompts\07-reels-top-hooks.md
OK   prompts\08-reels-retention-script.md
OK   prompts\09-reels-save-and-share.md
OK   prompts\10-reels-revival.md
OK   prompts\11-reels-strategic-trends.md
OK   prompts\12-reels-seven-day-test-matrix.md
OK   README.en.md
OK   README.md
OK   REVIEW.md
OK   ROADMAP.en.md
OK   ROADMAP.md
OK   SECURITY.md
OK   workflow\content_pipeline.md

29 Markdown files checked, 0 with broken links.
==> git diff --check (unstaged)
==> git diff --cached --check (staged)
dev_check: all gates passed
```

---

## 5. 安全與合規性檢核 (Security Compliance)

- [x] **無私鑰/Token 洩漏**：全代碼庫無任何硬編碼 API Key、憑證或敏感字串。
- [x] **零第三方 pip 依賴**：完全基於 Python 3.10+ 原生標準庫，無供應鏈投毒風險。
- [x] **純本機離線優先**：預設不向外部發起任何網路請求，數據不離機。
- [x] **跨平台路徑與換行規範**：全專案配置 `.editorconfig` (LF, UTF-8) 與 `.gitattributes`，Python 程式碼全面採用 `pathlib.Path`。
- [x] **GitHub 遠端操作防護**：所有 PR / Push / Release 嚴格限定只對齊 `SanHsien/ig-growth-prompts`。
