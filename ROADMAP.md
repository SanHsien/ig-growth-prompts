# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-10-29 依 `main` `33e96e826bb9` 查的快照，開工前先重查 GitHub。

## 現況

本 repo 是工具中立、純標準庫的 Instagram 提示詞與本機內容工作流，含 GUI、批次處理與日曆匯出（`AGENTS.md:7-12`、`README.md:44-66`）。2026-10-29 快照中 open issue／PR、Dependabot／code scanning 告警均為 0，CI、CodeQL、Dependency freshness 與排程批次最近結果為 success（2026-10-29 `gh` 查詢，`33e96e826bb9`）。本輪已將檢查點改為同目錄暫存檔加原子替換，並以寫入／替換失敗注入測試驗證舊狀態與 `--resume`；批次失敗策略取捨仍保留（深掃報告，2026-10-26，〈刻意不修〉）。

## 近期：可以直接動手

| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 補 Windows GUI 正常操作驗收 | 深掃未開視窗，尚不能代表桌面使用路徑已實測 | 在 Windows 原生 GUI 以單一測試主題走 manual 回覆、續跑、日曆匯出及含空白路徑的排程腳本；記錄結果與 SHA，不呼叫遠端 API | 維護者 | 深掃報告（2026-10-26）範圍說明；`REVIEW.md:71`；`README.md`〈桌面 GUI 工作台〉 |

## 中期：等條件成立再做

| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| Webhook 觸發與通知的明確介面 | 維護者選定 Zapier／Make／n8n 其中一個用途並授權外部連線 | 先定義輸入、認證、重送去重與離線預設；本機模擬成功、拒絕及重送，核准後才驗證一次外部通知 | Claude Opus | 接續開發報告（2026-10-25）〈刻意不做／延後〉；`AGENTS.md:11-12` |
| 定義批次失敗後的部分結果保留策略 | 出現需要保留前段成果、繼續其餘主題的實際案例 | 先記錄 fail-fast／continue 選擇；以中間主題失敗驗證 manifest、錯誤摘要與續跑不重複已完成主題 | Claude Sonnet | 深掃報告（2026-10-26）〈刻意不修〉；`igprompts/batch.py:128-136` |
| 固定 GUI 建置工具版本 | 維護者要求建置環境可重現或出現打包回歸 | 記錄 Python、PyInstaller 與安裝器版本；乾淨 Windows 環境產出 portable／setup 並各啟動一次 | Codex | `.github/workflows/release_gui.yml:74`；接續開發報告（2026-10-25）〈刻意不做／延後〉 |

## 刻意不做

| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 為通過稽核壓縮歷史或強推 | 保留 release tag 與歷史關係；已有保留歷史的決定，見 `CHANGELOG.md:15` | 維護者明確要求並另行評估歷史與 release 影響 |
| 核心加入第三方套件或預設遠端模型呼叫 | 違反核心純標準庫、本機運作的界線 | 維護者明確變更 `AGENTS.md` 的產品限制 |
| 把 dry-run 日曆當成正式發布或自動發文 | dry-run 是明確標示的展示輸出；現有工作流主要產生本機產物 | 確有發布需求，並先定義確認、憑證與誤發布防護 |

## 維護方式

每月查看 Dependency freshness；開工以 `gh pr list --repo SanHsien/ig-growth-prompts` 與 `gh api repos/SanHsien/ig-growth-prompts/dependabot/alerts?state=open` 重查，保留下限理由見 `pyproject.toml:2`。
功能或修復發版前跑 `pwsh -File tools/dev_check.ps1`，依 repo 規範同步中英說明與變更紀錄；其他文件只連結本路線圖，不另列後續計畫。
