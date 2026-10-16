# 安全政策 (Security Policy)

## 支援版本

| 版本 | 支援狀態 |
| :--- | :--- |
| `0.6.x` | :white_check_mark: 支援中 |
| `< 0.6.0` | :x: 已停止支援 |

## 敏感資訊保護原則

1. **嚴禁提交憑證**：
   - 任何 API Key、Token、私鑰、密碼不得寫入原始碼、指令列、範例檔或 Commit 歷史中。
2. **本機隔離原則**：
   - 工作流檔案與產出請儲存於本機工作區目錄，避免漫遊或存取非專案範圍之敏感檔案。

## 漏洞通報

若您在本專案中發現潛在的安全漏洞，請勿公開提交 Issue。請透過 GitHub 私密安全通報（Security Advisories）或聯繫維護者：
- GitHub: [@SanHsien](https://github.com/SanHsien)
- 專案倉庫: [`SanHsien/ig-growth-prompts`](https://github.com/SanHsien/ig-growth-prompts)

我們將在收到通報後盡速審核並修復。
