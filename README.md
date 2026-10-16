[English](README.en.md) | 中文版

# Instagram 爆款與不露臉內容經營 Prompt 框架庫 (IG Growth Prompts)

本專案收錄並深度拆解社群創作者 `@jasonxtsai` 所分享的「Claude IG Prompt 系列」。這套架構將帳號在兩個月內從零拉升至 6 萬追蹤、800 萬次觀看的精華工作流，抽象化為 5 個高度標準化、可隨插即用的 Prompt 模組，並附帶純 Python 標準庫（零第三方依賴）的命令列工具，協助創作者與開發者快速生成個人化的高品質貼文腳本。

---

## 專案特色

- **零依賴輕量設計**：核心套件 `igprompts` 僅使用 Python 標準函式庫（stdlib-only），無需 `pip install` 任何套件即可直接運作。
- **5 大結構化 Prompt 模組**：涵蓋防套路選題、15 句 5 型 Hook、3 種不露臉載體、留存完讀改寫、低調懂行權威感。
- **自動化工作流引擎（State Machine）**：支援階段執行、檢查點保存（Checkpointing）、斷點續跑（Resume）與自訂 Provider。
- **純本地向量 SVG 圖卡產生器**：零依賴輸出 1080x1350（Instagram 4:5 最佳直式比例）深色主題輪播圖卡集。
- **清楚的演進路線圖**：規劃 Phase 1~4 的自動化工作流演進藍圖，詳見 [ROADMAP.md](ROADMAP.md)。
- **嚴謹工程規範**：包含 Windows 原生品質檢查閘門（`tools/dev_check.ps1`）、Markdown 連結離線檢驗、雙語文件與 GitHub Actions CI。

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
│   ├── models.py                       # Prompt 定義與中繼資料
│   ├── renderer.py                     # 純本地 SVG 4:5 輪播圖卡渲染器
│   └── workflow.py                     # 工作流引擎、狀態機與 Provider
├── prompts/                            # 5 大核心 Prompt 規格與逐字稿
│   ├── 01-niche-ideation.md            # Prompt 1: 利基選題與防套路原創發想
│   ├── 02-hook-generator.md            # Prompt 2: 15 句 5 大類型開場 Hook 生成器
│   ├── 03-faceless-formats.md          # Prompt 3: 3 種不露臉高觸及內容改造
│   ├── 04-retention-optimization.md    # Prompt 4: 留存率、完讀率與互動指標優化
│   └── 05-authority-positioning.md     # Prompt 5: 不吹噓的個人品牌專業權威改寫
├── workflow/
│   └── content_pipeline.md             # 5 階段自動化內容生產 SOP 與系統化擴展
├── examples/
│   └── sample_inputs.json              # 示範輸入參數設定檔
├── tests/                              # 單元測試套件
│   ├── test_cli.py
│   ├── test_prompts.py
│   ├── test_renderer.py
│   └── test_workflow.py
└── tools/                              # 工程維護與檢測工具
    ├── check_links.py                  # Markdown 相對連結離線檢查
    └── dev_check.ps1                   # Windows 原生 Canonical Quality Gate
```

---

## CLI 工具快速上手

### 1. 列出所有可用的 Prompt 與必要參數
```bash
python -m igprompts list
```
輸出範例：
```text
ID   Key                      Title                          Required Variables
------------------------------------------------------------------------------------------
1    niche_ideation           利基市場防套路與原創點子       niche, audience, goal
2    hook_generator           15 句 5 種類型開場 Hook 生成器 idea, audience, tone
3    faceless_formats         3 種不露臉高觸及內容改造       idea, audience, goal
4    retention_optimization   留存率、完讀率與互動指標優化   content, voice, audience
5    authority_positioning    不吹噓的個人品牌專業權威改寫   content, audience, brand_voice
```

### 2. 檢視原始 Prompt 模板
```bash
python -m igprompts show 1
```

### 3. 填入變數產生即用 Prompt
你可以直接在命令列指定變數，或讀取 JSON 設定檔：
```bash
# 透過命令行變數生成 Prompt 1
python -m igprompts render 1 \
  --var niche="AI 軟體架構" \
  --var audience="資深工程師與技術主管" \
  --var goal="建立技術公信力與諮詢漏斗"

# 或從 JSON 設定檔生成
python -m igprompts render 1 --json-file examples/sample_inputs.json
```

### 4. 一鍵匯出端到端 5 階段 Pipeline
```bash
python -m igprompts pipeline --json-file examples/sample_inputs.json -o pipeline_output.md
```

### 5. 自動化執行工作流並產生 SVG 圖卡（Phase 1 & 2）
```bash
# 執行工作流狀態機，產出 state.json、manifest.md，並生成 4:5 輪播 SVG 圖卡
python -m igprompts run-pipeline \
  --json-file examples/sample_inputs.json \
  --output-dir output_run \
  --render-slides
```
輸出結果：
- `output_run/workflow_state.json`：包含每一步的狀態、輸入、輸出與時間戳記。
- `output_run/pipeline_manifest.md`：排版整齊的貼文總結與交付物。
- `output_run/slides/slide_01.svg` ~ `slide_05.svg`：純本地向量圖卡，可直接在瀏覽器預覽或匯入設計軟體。

### 6. 直接產出 1080x1350 向量輪播圖卡
```bash
python -m igprompts render-slides --json-file examples/sample_inputs.json --output-dir my_slides
```

---

## 5 大核心 Prompt 快速檢索

| 編號 | 階段定位 | 核心角色 | 關鍵任務 | 詳細規格 |
|:---|:---|:---|:---|:---|
| **1** | **選題防套路** | 10 年成長顧問 (帶過 50 個 10 萬粉帳號) | 先列 7 個看膩套路，再給 10 個原創點子，評選前 3 名 | [01-niche-ideation.md](prompts/01-niche-ideation.md) |
| **2** | **Hook 鉤子** | 爆款文案操盤手 (完播率 +40%) | 輸出 15 句 Hook (懸念/逆向/情緒/數據/內行)，限 15 字，評選最強 5 句 | [02-hook-generator.md](prompts/02-hook-generator.md) |
| **3** | **不露臉改編** | 不露臉內容操盤師 | 展開為輪播、純字幕 Reel、無聲視覺貼文，附逐幕逐頁文字與視覺配色 | [03-faceless-formats.md](prompts/03-faceless-formats.md) |
| **4** | **留存率優化** | 留存率優化顧問 | 刪除軟弱句與廢話，每行收尾埋鉤子，拉高完讀、收藏與分享 | [04-retention-optimization.md](prompts/04-retention-optimization.md) |
| **5** | **權威感定位** | 個人品牌定位顧問 | 去大師腔、不堆砌成績，產出「質感版、俐落版、高級版」懂行者實話 | [05-authority-positioning.md](prompts/05-authority-positioning.md) |

完整的端到端生產 SOP 請參考 [workflow/content_pipeline.md](workflow/content_pipeline.md)。

---

## 值得參考的核心思維（Prompt Engineering 視角）

1. **「先破後立」的負面約束（Negative Constraint First）**
   - 普遍提問直接問「給我 10 個點子」，模型容易產出平庸內容。Prompt 1 先要求「列出 7 種看膩的套路」，讓模型在思考前建立過濾邊界，大幅提升原創度。
2. **多維度分類矩陣（Categorical Taxonomy）**
   - Prompt 2 將 Hook 嚴格細分成 5 種類型（懸念／逆向／情緒／數據／內行），避免模型只會產出一種調性的句子，給創作者豐富的 A/B 測試空間。
3. **消除模型感與爹味（Anti-AI & Anti-Guru Tone）**
   - 明確加入「要像真人在講話，沒有 AI 味」、「沒有說教感、沒有大師腔、不堆數字秀成績」，精準避開大語言模型容易出現的空泛辭藻與好為人師的口氣。
4. **輸出即產品（Production-Ready Deliverables）**
   - 包含畫面逐字稿、視覺搭配建議、Caption、CTA、排名前三理由與改寫對照，所有輸出可直接丟進 Canva、剪映或排程工具中發布。

---

## 我可以仿照做什麼（實踐行動指南）

### 1. 打造技術／知識型個人的「不露臉」自媒體
- **工程師／技術人痛點**：不想露臉、沒時間拍片、討厭浮誇行銷。
- **具體實踐**：
  - 挑選平日遇到的技術坑、架構決策或開發心得作為素材。
  - 套用 Prompt 3 生成「輪播圖卡（Code/Architecture Slide）」或「純文字短片」。
  - 透過 Prompt 5 修飾成低調懂行的語氣，在 Threads、IG、LinkedIn 建立專業形象。

### 2. 結合排程與圖卡渲染打造自動化管線
- 利用本專案提供的 `igprompts` 模組：
  - 傳入主題關鍵字或 Note 筆記。
  - 串接 Playwright 或 Satori 自動將 Prompt 3 的逐頁文字渲染成社群圖卡（SVG / PNG）。
  - 搭配定時發布工具，達成低維護成本的知識內容輸出。

---

## 本地開發與驗證閘門

所有修改必須通過 Windows Canonical Quality Gate：

```powershell
pwsh -File tools/dev_check.ps1
```

執行項目包括：
1. **單元測試**：`python -m unittest discover -s tests -p "test_*.py" -v`
2. **連結檢查**：`python tools/check_links.py`（驗證所有 Markdown 相對連結與圖片）
3. **Git 空白與換行檢查**：`git diff --check`

---

## 授權與致謝

- 原始概念與 Prompt 架構：`@jasonxtsai` (Instagram)
- 專案架構、CLI 工具與工程化規範：[SanHsien](https://github.com/SanHsien)
- 授權條款：[MIT License](LICENSE)
