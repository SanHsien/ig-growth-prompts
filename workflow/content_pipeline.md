# 內容增長自動化生產線（Content Pipeline SOP）

本指南說明如何將這 5 個 Prompt 串聯成一條完整的「端到端（End-to-End）自媒體生產管線」，無論手動批次執行或使用 Agent 自動化皆可無縫套用。

```
[Prompt 1: 選題防套路] 
       │ 產出 10 個原創選題，挑選 Top 3
       ▼
[Prompt 2: Hook 爆款測試]
       │ 針對選中主題生成 15 句 Hook (5大類)，選出最強 1~2 句
       ▼
[Prompt 3: 不露臉多模態改編]
       │ 展開成輪播圖 / 純字幕短片 / 視覺慢動態，取得每頁腳本與視覺建議
       ▼
[Prompt 4: 留存率與滑梯改寫]
       │ 磨光文字：去軟弱句、加強每行鉤子、優化完讀與收藏 CTA
       ▼
[Prompt 5: 權威感與調性修飾]
       │ 拿掉 AI 味與大師腔，微調成質感／俐落／高級版，最終發布
```

---

## 階段一：選題與定位（Ideation & Positioning）

- **工具**：`prompts/01-niche-ideation.md`
- **輸入**：
  - 利基領域（例如：全端工程師成長、AI 自動化工作流、獨立開發者變現）
  - 受眾（初中階開發者、想提升效率的技術創作者）
  - 目標（吸引高黏著追蹤、建立顧問諮詢漏斗）
- **交付物**：10 個反直覺的選題清單 + 前 3 名爆款潛力主題。

---

## 階段二：開頭注意力爭奪（Hook Crafting）

- **工具**：`prompts/02-hook-generator.md`
- **輸入**：選中的主題 + 目標受眾 + 說話語氣。
- **交付物**：15 句小於 15 字的 Hook（懸念、逆向、情緒、數據、內行），從中挑出點擊率最高的首頁大字。

---

## 階段三：多渠道載體生成（Format Adaptation）

- **工具**：`prompts/03-faceless-formats.md`
- **輸入**：主題創意 + 受眾 + 期望效益。
- **交付物**：
  - 輪播貼文（Carousel，適合 IG / LinkedIn）
  - 純字幕短片（Reels / TikTok / YouTube Shorts）
  - 靜態視覺金句（Threads / X）

---

## 階段四：深度優化與留存攻防（Retention & Conversion Polish）

- **工具**：`prompts/04-retention-optimization.md` + `prompts/05-authority-positioning.md`
- **輸入**：初稿內容與品牌語氣。
- **交付物**：
  - 刪除多餘形容詞與說教語氣，營造實戰老手娓娓道來的信服力。
  - 設計高收藏動機（例如檢核表、指令庫、參考框架）。

---

## 自動化與程式碼整合可能（Engineering Extension）

1. **CLI / Python 批次腳本**：
   - 建立 CLI 工具，傳入主題名稱後，調用 LLM API 連鎖執行 1~5 步驟，直接輸出 Markdown 腳本。
2. **自動圖文合成（Headless Rendering）**：
   - 串接 Playwright 或 Satori / Puppeteer，將 Prompt 3 的逐頁文字自動渲染成質感社群圖卡（SVG / PNG）。
3. **排程監控與發布**：
   - 配合社群 API 或排程工具（如 Buffer / Make），實現定時生產與分發。
