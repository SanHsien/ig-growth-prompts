# GEMINI.md - Antigravity Agent Guidelines

本文件為 Google Antigravity / Gemini Agent 在本倉庫（`SanHsien/ig-growth-prompts`）協作的專用指引。

## 核心原則

1. **繁體中文回覆**：對話與回報一律使用繁體中文，技術術語、API、檔案名保留英文原文。
2. **Windows 11 原生假設**：本機為 Windows 11 原生環境（非 WSL），路徑使用 Windows 正確反斜線/正斜線處理，嚴禁假設 POSIX 環境指令（如裸跑 `cat` 或 `grep`）。
3. **嚴禁偽造或留 TODO**：
   - 不寫假資料或假空殼。空白數據標記為未填（`—`），絕不擅自捏造成 0。
   - 不留 `// TODO` 或未實作函式。
4. **驗證硬閘門**：
   - 每次修改程式碼或文件後，必須在本地跑過驗證閘門：
     ```powershell
     pwsh -File tools/dev_check.ps1
     ```
   - 報告結論時必須附上該指令的實際執行輸出。
5. **PR / Push 專一性**：
   - PR、push、release 一律只打 `SanHsien/ig-growth-prompts`，絕不對外打到任何上游或無關帳號。
6. **零外部依賴原則**：
   - 核心函式庫 `igprompts/` 僅依賴 Python 3.10+ 標準庫（stdlib-only），零 pip 第三方套件依賴。
