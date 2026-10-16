# 安全政策 (Security Policy)

## 支援版本 (Supported Versions)

| 版本 | 支援狀態 |
| :--- | :--- |
| `main` 分支最新代碼 | :white_check_mark: 支援中 |
| `v0.6.x` (最新發布版) | :white_check_mark: 支援中 |
| `< 0.6.0` | :x: 已停止支援 |

---

## 回報安全性弱點 (Reporting a Vulnerability)

若您發現本專案存在任何潛在的安全風險、漏洞或憑證外洩隱患，請**切勿**直接建立公開的 Issue 或於討論區張貼。

請使用 GitHub 官方私密安全通報機制：

**[:lock: 點此提交私密安全諮詢 (GitHub Security Advisory)](https://github.com/SanHsien/ig-growth-prompts/security/advisories/new)**

您亦可前往專案倉庫頁面的 **Security** 標籤頁，點選 **Report a vulnerability** 進行通報。

通報內容請盡可能包含：
- 受影響的組件（例如：CLI、GUI、Provider 接口、工作流解析）與版本號
- 重現步驟與概念驗證（PoC / Reproduction Steps）
- 潛在影響範圍與威脅評估
- 建議之緩解或修復措施（如有）

專案維護者將在確認問題後評估影響範圍，並儘速於受支援的分支發布安全性修復。

---

## 核心安全架構與防禦性設計 (Security & Quality Architecture)

本專案在設計之初即貫徹嚴格的防禦性安全標準：

1. **純 Python 標準庫（Zero Third-Party pip Dependencies）**：
   - 核心套件 `igprompts` 與測試集完全依賴 Python 3.10+ 原生標準庫（`dataclasses`, `json`, `csv`, `urllib`, `tkinter` 等），從源頭根除第三方套件可能引入的供應鏈投毒（Supply-chain attack）或隱蔽後門風險。
2. **純本地離線運作與零遙測（Zero Telemetry & Offline First）**：
   - 系統不會向任何未經授權的伺服器傳送統計數據、追蹤代碼或使用者輸入內容。
   - 提示詞渲染、排程隊列生成、成效報表試算、Markdown / CSV / SVG 匯出皆在本地沙箱與記憶體內完成。
3. **敏感資訊與憑證隔離保護**：
   - 嚴禁將任何 API Key、Token、私鑰寫入原始碼、設定檔或 Commit 歷史。
   - 若使用可選之自動化 Provider（如 OpenAI、Anthropic 等相容接口），憑證一律透過作業系統環境變數（如 `OPENAI_API_KEY`）讀取，且不會以明文形式寫入 `workflow_state.json` 或本機紀錄檔。
4. **檔案系統寫入邊界約束**：
   - CLI 與 GUI 輸出一律限制在使用者指定的工作目錄或暫存目錄中，禁止越權讀寫專案目錄外之機敏路徑。
