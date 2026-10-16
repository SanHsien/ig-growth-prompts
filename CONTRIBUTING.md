# 貢獻指南 (Contributing Guide)

感謝您對 `ig-growth-prompts` 專案的關注！本專案採用嚴謹的工程規範與自動化治理。

## 核心守則

1. **零第三方執行期依賴（Zero Dependencies）**：
   - 核心函式庫 `igprompts/` 必須純以 Python 3.10+ 標準庫（stdlib）撰寫，不得引入外部 pip 依賴。
2. **AI 工具中立性（Model & Agent Agnostic）**：
   - 任何新增的 Prompt 或工作流擴展，不得硬編碼特定廠商模型。
3. **實證原則（No Dummy / No Hallucination）**：
   - 空白數據保留為未測（`—`），絕不擅自填 0 或偽造資料。
   - 渲染模組必須嚴格解析真實規格（如 ````slides` 區塊），無規格時明確報錯。

## 本地開發與驗證

提交 Pull Request 之前，必須在 Windows 原生環境通過所有品質閘門：

```powershell
pwsh -File tools/dev_check.ps1
```

品質閘門驗證項目：
1. **單元測試**：所有單元測試必須 100% 通過（`python -m unittest discover -s tests -p "test_*.py" -v`）。
2. **Markdown 連結檢查**：`python tools/check_links.py` 驗證所有文件相對連結與錨點。
3. **Git 空白規範**：`git diff --check` 不得包含多餘的行尾空白或檔案末端空行。

## 提交規範

- PR 與 Push 請僅指向本倉庫：[`SanHsien/ig-growth-prompts`](https://github.com/SanHsien/ig-growth-prompts)。
- Commit 訊息建議遵循 [Conventional Commits](https://www.conventionalcommits.org/)（例如 `feat: ...`, `fix: ...`, `docs: ...`）。
