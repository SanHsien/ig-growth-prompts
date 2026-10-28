# AGENTS.md

給所有 AI agent 的規範（單一真相源）。

## 這個 repo 是什麼

`ig-growth-prompts`：Instagram 爆款與不露臉內容經營 Prompt 框架庫，包含結構化 Prompt 規格、端到端內容生產管線（SOP），以及零第三方依賴的 Python 命令列工具與驗證套件。

## 硬槓槓（不可放寬）

- **純本機、零外部依賴**：核心函式庫 `igprompts/` 只使用 Python 3.10+ 內建標準庫（stdlib-only），禁止加入未經許可的第三方套件依賴。
- **不私自聯網發送請求**：Prompt 生成與文字替換均在本地完成，不私自調用遠端 API。
- **文件與多語同步**：新增功能或修改規格時，必須同步更新 `README.md`、`README.en.md`、`CHANGELOG.md` 與 `CHANGELOG.en.md`。
- **無假程式碼與空殼**：禁止留下 TODO、假測試或空殼函式。不寫假資料；空白數據標記為未填（`—`），不擅自捏造成 0。
- **驗證先行**：宣稱「完成／修好／測試通過」之前，必須在目標環境（Windows 11 原生）執行過檢查，並在回覆中附上實際輸出。

## 回覆與環境

- 回覆一律用繁體中文，先結論後細節，不說客套話；技術術語、API、檔案名保留英文原文。
- Windows 11 原生環境（非 WSL），不用 POSIX 假設（例如不裸跑 `cat`、`grep`），路徑分隔符要正確處理。

## 慣例

- 檔案編碼一律 UTF-8，換行一律 LF（透過 `.gitattributes` 與 `.editorconfig` 保證）。
- 所有 Markdown 中的相對連結必須指向實際存在的檔案，由 `tools/check_links.py` 保證不失效。
- 提交前必須跑過 `tools/dev_check.ps1`。

## 驗證

```bash
# 跨平台 / Linux
python -m unittest discover -s tests -p "test_*.py" -v
python tools/check_links.py
```

Windows：
```powershell
pwsh -File tools/dev_check.ps1
```

驗證全部通過才提交。直接推 `main`，不開分支、不開 PR。PR、push、release 一律只打 `SanHsien/ig-growth-prompts`，不打到任何上游或無關帳號。

## 路線圖

- `ROADMAP.md` 是本 repo 後續工作的單一真相源。完成或新增工作時，在同一個 commit 更新它：做完的列刪掉、新工作加進去。不要在其他文件另列待辦。
