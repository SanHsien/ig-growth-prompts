[English](README.en.md) | 中文版

# Instagram 爆款與不露臉內容經營 Prompt 框架庫 (IG Growth Prompts)

本專案收錄並深度拆解社群創作者 `@jasonxtsai` 所分享的 Instagram 爆款成長體系（包含圖文/輪播/不露臉與短影音兩大實戰路徑）。我們將其抽象化為 **12 組全局統一編號（01 ~ 12）** 的結構化 Prompt 模組，並附帶純 Python 標準庫（零第三方依賴）的工作流引擎、7 天測試帳本與 SVG 圖卡排版工具。

> [!IMPORTANT]
> **AI 工具與 Agent 中立（Model & Agent Agnostic）**
> 本專案的所有 Prompt 與自動化工具完全中立，不綁定特定廠商或 Agent。你可以自由搭配手邊最熟練、屬意的任何 AI 工具使用：不論是網頁聊天（Claude, ChatGPT, Gemini, DeepSeek, v0）、本機模型（Ollama, LLaMA）、命令列工具（`llm`, `claude -p`）還是自建的 AI Coding Agent。

---

## 專案特色

- **零依賴輕量設計**：核心套件 `igprompts` 僅使用 Python 標準函式庫（stdlib-only），無需 `pip install` 任何套件即可直接運作。
- **12 組全局統一編號 Prompt 模組**：
  - **系列 1（01 ~ 05）**：圖文與不露臉精準留存體系（防套路選題、15 字 Hook、不露臉改編、滑梯文案、低調專業定位）。
  - **系列 2（06 ~ 12）**：短影音爆款與假設驗證體系（7 天題目、1~3 秒 Hook、分鏡腳本、轉發動機、數據診斷、策略跟風、7 天測試矩陣）。
- **靈活可插拔的 Provider**：
  - `manual`：在 `handoff/` 產出檔案，供任何聊天介面複製貼上，並以 `--resume` 續跑。
  - `command`：透過標準輸入輸出（stdin/stdout）串接任何本機 CLI 工具（如 `ollama run` 或自訂指令）。
  - `dry-run`：離線驗證，明確標記 `[dry-run]`，絕不捏造假資料。
- **純本地向量 SVG 圖卡產生器**：零依賴輸出 1080x1350（Instagram 4:5 最佳直式比例）深色主題輪播圖卡集。
- **7 天測試帳本與復盤閉環**：Prompt 12 規劃測試 -> CSV 帳本填入後台數據 -> 自動計算指標 -> 餵入 Prompt 10 進行診斷與重寫。
- **演進路線圖**：完整記錄工作流演進藍圖，詳見 [ROADMAP.md](ROADMAP.md)。

---

## 專案目錄結構

```
ig-growth-prompts/
├── .github/workflows/ci.yml            # 跨平台 CI 工作流程 (Windows + Ubuntu)
├── .editorconfig                       # 縮排與編碼規範 (UTF-8, LF)
├── .gitattributes                      # Git 換行統一規範 (eol=lf)
├── .gitignore                          # Python / IDE 忽略檔案清單
├── AGENTS.md                           # AI Agent 規範（單一真相源）
├── CLAUDE.md                           # Claude 專屬提示與驗證指引
├── CHANGELOG.md                        # 中文變更紀錄 (Keep a Changelog)
├── CHANGELOG.en.md                     # 英文變更紀錄
├── LICENSE                             # MIT 授權條款
├── README.md                           # 繁體中文說明文件
├── README.en.md                        # 英文說明文件
├── ROADMAP.md                          # 自動化工作流演進路線圖
├── ROADMAP.en.md                       # 英文路線圖
├── igprompts/                          # 核心 Python 套件 (stdlib-only)
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py                          # 命令列介面實作
│   ├── core.py                         # 模板檢索與變數渲染
│   ├── experiments.py                  # 7 天測試帳本與復盤分析
│   ├── models.py                       # 統一 01~12 Prompt 定義
│   ├── providers.py                    # 工具中立 Provider (Manual, Command, DryRun)
│   ├── renderer.py                     # 純本地 SVG 4:5 輪播圖卡渲染器
│   └── workflow.py                     # 工作流引擎與狀態機
├── prompts/                            # 12 大核心 Prompt 規格與逐字稿 (全局統一編號)
│   ├── 01-niche-ideation.md            # Prompt 01: 利基選題與防套路原創發想
│   ├── 02-hook-generator.md            # Prompt 02: 15 句 5 大類型開場 Hook 生成器
│   ├── 03-faceless-formats.md          # Prompt 03: 3 種不露臉高觸及內容改造
│   ├── 04-retention-optimization.md    # Prompt 04: 留存率、完讀率與互動指標優化
│   ├── 05-authority-positioning.md     # Prompt 05: 不吹噓的個人品牌專業權威改寫
│   ├── 06-reels-7day-topics.md         # Prompt 06 (Reels 1): 找出未來 7 天最該拍的題目
│   ├── 07-reels-top-hooks.md           # Prompt 07 (Reels 2): 找出最強的開場鉤子
│   ├── 08-reels-retention-script.md    # Prompt 08 (Reels 3): 把題目寫成留得住人的短影音腳本
│   ├── 09-reels-save-and-share.md      # Prompt 09 (Reels 4): 讓人想收藏，也想傳給朋友
│   ├── 10-reels-revival.md             # Prompt 10 (Reels 5): 把發過的 Reels 重新救回來
│   ├── 11-reels-strategic-trends.md    # Prompt 11 (Reels 6): 跟風要跟得有策略
│   └── 12-reels-seven-day-test-matrix.md # Prompt 12 (Reels 7): 排出你的 7 天測試表
├── workflow/
│   └── content_pipeline.md             # 內容生產 SOP 與系統化擴展
├── examples/
│   ├── sample_inputs.json              # 示範輸入參數設定檔 (支援 1~12 題變數)
│   └── sample_slides.md                # 輪播圖卡規格範例
├── tests/                              # 單元測試套件 (31 個測試全通過)
│   ├── test_cli.py
│   ├── test_experiments.py
│   ├── test_prompts.py
│   ├── test_renderer.py
│   └── test_workflow.py
└── tools/                              # 工程維護與檢測工具
    ├── check_links.py                  # Markdown 相對連結離線檢查
    └── dev_check.ps1                   # Windows 原生 Canonical Quality Gate
```

---

## 12 組核心 Prompt 總覽

### 系列 1：圖文與不露臉精準留存體系 (Prompts 01 ~ 05)

| 編號 | 階段定位 | 核心角色 | 關鍵任務 | 詳細規格 |
|:---|:---|:---|:---|:---|
| **01** | **選題防套路** | 10 年成長顧問 (帶過 50 個帳號) | 先列 7 個看膩套路，再給 10 個原創點子，評選前 3 名 | [01-niche-ideation.md](prompts/01-niche-ideation.md) |
| **02** | **Hook 鉤子** | 爆款文案操盤手 (完播率 +40%) | 輸出 15 句 Hook (懸念/逆向/情緒/數據/內行)，限 15 字，評選最強 5 句 | [02-hook-generator.md](prompts/02-hook-generator.md) |
| **03** | **不露臉改編** | 不露臉內容操盤師 | 展開為輪播、純字幕 Reel、無聲視覺貼文，附逐幕逐頁文字與視覺配色 | [03-faceless-formats.md](prompts/03-faceless-formats.md) |
| **04** | **留存率優化** | 留存率優化顧問 | 刪除軟弱句與廢話，每行收尾埋鉤子，拉高完讀、收藏與分享 | [04-retention-optimization.md](prompts/04-retention-optimization.md) |
| **05** | **權威感定位** | 個人品牌定位顧問 | 去大師腔、不堆砌成績，產出「質感版、俐落版、高級版」懂行者實話 | [05-authority-positioning.md](prompts/05-authority-positioning.md) |

### 系列 2：短影音爆款與假設驗證體系 (Prompts 06 ~ 12)

| 編號 | 階段定位 | 核心角色 | 關鍵任務 | 詳細規格 |
|:---|:---|:---|:---|:---|
| **06** | **7 天選題** | Reels 策略顧問 | 結合粉絲數與階段目標，產生 7 天高需求、原創短影音題目 | [06-reels-7day-topics.md](prompts/06-reels-7day-topics.md) |
| **07** | **最強開場** | 爆款短影音鉤子文案 | 產出 20 個前 1~3 秒短影音鉤子（涵蓋 8 大機制），評選前 5 名 | [07-reels-top-hooks.md](prompts/07-reels-top-hooks.md) |
| **08** | **完播腳本** | 完播率腳本編導 | 包含開場、分鏡、口播逐字稿、字卡、切鏡、價值段、秒數標註 | [08-reels-retention-script.md](prompts/08-reels-retention-script.md) |
| **09** | **裂變轉發** | 社群裂變傳播顧問 | 實用/認同/情緒/意外/解題 5 角度，「傳出去像在幫朋友一個忙」 | [09-reels-save-and-share.md](prompts/09-reels-save-and-share.md) |
| **10** | **數據復盤** | 數據覆盤與改寫顧問 | 區分確定結論 vs 不亂猜盲點，提煉 Top 3 改善點並重寫腳本 | [10-reels-revival.md](prompts/10-reels-revival.md) |
| **11** | **策略跟風** | 趨勢策略分析師 | 拆解「機制 ≠ 影片」，移植趨勢機制到垂直領域，排除過度飽和 | [11-reels-strategic-trends.md](prompts/11-reels-strategic-trends.md) |
| **12** | **測試矩陣** | 成長實驗排程顧問 | 排出 7 天正交差異化測試表，標註驗證假設與監控指標 | [12-reels-seven-day-test-matrix.md](prompts/12-reels-seven-day-test-matrix.md) |

---

## CLI 工具操作指引

### 1. 檢索與渲染 Prompt
```bash
# 列出全部 12 個 Prompt
python -m igprompts list

# 篩選短影音系列 (Prompts 06-12)
python -m igprompts list --series reels

# 檢視原始 Prompt 模板
python -m igprompts show 06

# 填寫變數產出即用文字（可複製到任何 AI 聊天介面）
python -m igprompts render 06 --json-file examples/sample_inputs.json
```

### 2. 手動交接模式（與任何 Web AI 協作）
如果你習慣使用 ChatGPT, Claude.ai, Gemini 或任何網頁聊天工具：
```bash
python -m igprompts run-pipeline \
  --series faceless \
  --json-file examples/sample_inputs.json \
  --provider manual \
  -o my_work
```
執行後程式會在 `my_work/handoff/` 產生 `01-niche_ideation.prompt.md`：
1. 將內容複製貼進你喜愛的 AI 工具中取得回覆。
2. 將 AI 回覆儲存為 `01-niche_ideation.response.md`。
3. 再次執行 `python -m igprompts run-pipeline --resume --provider manual -o my_work`，流水線即會讀取回覆並自動推進至下一步！

### 3. 命令列管道模式（串接本機 CLI 或自訂 Agent）
如果你有安裝本地 LLM 或 CLI 工具（例如 Ollama 或自建指令）：
```bash
python -m igprompts run-pipeline \
  --series faceless \
  --json-file examples/sample_inputs.json \
  --provider command \
  --cmd "ollama run llama3" \
  -o my_work
```

### 4. 7 天測試帳本與復盤流程 (Phase 3)
```bash
# 步驟 A：依 Prompt 12 規劃產出空的 CSV 帳本
python -m igprompts experiment plan --csv ledger.csv

# 步驟 B：至 IG 後台將各支影片的真實觀看、收藏、分享數填入 ledger.csv

# 步驟 C：產出分析報告，並自動填入 Prompt 10 的輸入檔案
python -m igprompts experiment report \
  --csv ledger.csv \
  --output report.md \
  --prompt-out prompt10_input.txt
```
直接將 `prompt10_input.txt` 丟給任何 AI，即可立即取得診斷結論與重寫後的全新版本！

### 5. 純本地 1080x1350 輪播圖卡生成
```bash
# 從規格檔案生成高品質 SVG 圖卡集
python -m igprompts render-slides --from examples/sample_slides.md -o slides_out
```

### 6. 多渠道內容發布日曆 (Phase 4)
支援將 7 天測試帳本或工作流狀態直接轉為發布排程，匯出 Notion Database、Airtable、Buffer (CSV) 及 Markdown 表格：
```bash
# 從 7 天測試帳本產生全渠道匯出檔案
python -m igprompts calendar generate \
  --from-ledger ledger.csv \
  --start-date 2026-11-01 \
  --format all \
  -o calendar_export

# 僅匯出 Notion CSV
python -m igprompts calendar generate \
  --from-ledger ledger.csv \
  --format notion \
  -o notion.csv
```

### 7. 主題庫批次執行 (Phase 4)
建立 JSON 或 CSV 隊列，自動批次跑完所有主題：
```bash
# 使用 JSON 隊列批次跑工作流
python -m igprompts batch run \
  -f examples/sample_topics_queue.json \
  --provider dry-run \
  -o batch_output
```

---

## 本地開發與驗證閘門

所有修改必須通過 Windows Canonical Quality Gate：

```powershell
pwsh -File tools/dev_check.ps1
```

執行項目包括：
1. **單元測試**：`python -m unittest discover -s tests -p "test_*.py" -v`（43 個單元測試）
2. **連結檢查**：`python tools/check_links.py`（驗證所有 Markdown 相對連結與錨點）
3. **Git 空白與換行檢查**：`git diff --check`

---

## 授權與致謝

- 原始概念與 Prompt 架構：`@jasonxtsai` (Instagram)
- 專案架構、CLI 工具與工程化規範：[SanHsien](https://github.com/SanHsien)
- 授權條款：[MIT License](LICENSE)
