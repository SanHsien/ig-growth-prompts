"""Prompt definitions and structured metadata across all supported series (Unified 01-12 IDs).

All prompts and workflows are strictly Model & Agent Agnostic.
They are fully compatible with any LLM, AI Agent, or interface (Claude, ChatGPT,
Gemini, DeepSeek, Local Ollama, Copilot, etc.).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PromptDefinition:
    id: int
    key: str
    series: str  # "faceless_carousel" or "short_video_reels"
    series_index: int
    title: str
    role: str
    variables: tuple[str, ...]
    template: str
    description: str


# ============================================================================
# Series 1: 圖文與不露臉精準留存體系 (Faceless & Carousel Series, ID 01 ~ 05)
# ============================================================================
FACELESS_CAROUSEL_PROMPTS: dict[int, PromptDefinition] = {
    1: PromptDefinition(
        id=1,
        key="niche_ideation",
        series="faceless_carousel",
        series_index=1,
        title="利基市場防套路與原創點子",
        role="操盤 IG 超過 10 年的成長顧問",
        variables=("niche", "audience", "goal"),
        template="""扮演一位操盤 IG 超過 10 年的成長顧問，
親手帶過 50 個帳號從 0 做到 10 萬追蹤。
你的任務：
研究我所在的利基市場，列出 7 種觀眾已經看膩、
會直接滑走的內容套路，
再給我 10 個跳脫這些套路、
又符合演算法邏輯的原創貼文點子。
每個點子都要寫清楚這 5 件事：
① 主軸概念（這篇想講什麼）
② 第一句 Hook（讓手指停住的開場）
③ 建議格式（輪播 / Reel / 單圖）
④ 新鮮感來源（跟別人哪裡不一樣）
⑤ 值得留下的理由（為什麼會收藏或轉發）
最後挑出最具爆發力的「前 3 名」，附上排序原因。
----------------------------------------
🎯 利基市場（Niche）= {niche}
👥 受眾（Audience）= {audience}
🚩 目標（Goal）= {goal}""",
        description="研究利基市場，排除 7 種看膩套路，產出 10 個反套路的原創貼文點子與前 3 名排序。",
    ),
    2: PromptDefinition(
        id=2,
        key="hook_generator",
        series="faceless_carousel",
        series_index=2,
        title="15 句 5 種類型開場 Hook 生成器",
        role="專寫 IG 爆款開頭的文案操盤手",
        variables=("idea", "audience", "tone"),
        template="""扮演一位專寫 IG 爆款開頭的文案操盤手，
你經手的 Hook 平均把完播率拉高 40%。
你的任務：
根據我提供的創意，寫出 15 句開場 Hook，
分成以下 5 種類型，每種各 3 句：
— 懸念型（讓人非知道答案不可）
— 逆向型（講出多數人沒想過的切角）
— 情緒型（戳到感受，讓人想往下看）
— 數據型（用一個具體數字讓人停住）
— 內行型（不張揚，一看就知道你懂）
Hook 撰寫規則：
— 禁止標題黨與誇大保證
— 要像真人在講話，沒有 AI 味
— 每句不超過 15 個字
— 最後選出最強的 5 句，逐一說明強在哪
----------------------------------------
💡 創意（Idea）= {idea}
👥 受眾（Audience）= {audience}
💬 語氣（Tone）= {tone}""",
        description="根據主題創意生成 15 句 Hook（5 種類型各 3 句），限 15 字且無 AI 味。",
    ),
    3: PromptDefinition(
        id=3,
        key="faceless_formats",
        series="faceless_carousel",
        series_index=3,
        title="3 種不露臉高觸及內容改造",
        role="IG 不露臉內容操盤師",
        variables=("idea", "audience", "goal"),
        template="""扮演一位 IG 不露臉內容操盤師，
專門協助不想出鏡，手邊沒有專業器材的創作者
做出高觸及的內容。
你的任務：
把我提供的創意，
改造成 3 種形式完全不同的不露臉版本：
版本一：輪播貼文
版本二：純字幕 Reel（畫面文字，不用配音）
版本三：無聲視覺貼文（靜態或慢動態）
每個版本都要給我：
① 完整結構（每一張／每一幕的內容）
② 畫面上的文字（逐字稿）
③ 視覺建議（背景、字體、配色）
④ 貼文說明文案（caption 寫法）
⑤ CTA（結尾怎麼引導留言或收藏）
限制：不出鏡，不配音，不追熱門，不用複雜剪輯
----------------------------------------
💡 創意（Idea）= {idea}
👥 受眾（Audience）= {audience}
🎯 目標（Goal）= {goal}""",
        description="將創意改編為輪播圖、純字幕 Reel、無聲視覺貼文 3 種不露臉版本，附逐頁逐幕規格。",
    ),
    4: PromptDefinition(
        id=4,
        key="retention_optimization",
        series="faceless_carousel",
        series_index=4,
        title="留存率、完讀率與互動指標優化",
        role="IG 留存率優化顧問",
        variables=("content", "voice", "audience"),
        template="""扮演一位 IG 留存率優化顧問，
你最擅長把平淡的內容改成讓人看到最後、
按下收藏、甚至回頭再看一次的版本。
你的任務：
改寫我提供的內容，同時把以下 4 個數據推到最高：
① 停留時間（讓人捨不得滑開）
② 完讀率（每一行都推著人看下一行）
③ 收藏數（讓人覺得「之後一定用得到」）
④ 分享數（讓人想「這要傳給朋友」）
改寫規則：
— 刪除所有軟弱句、廢話、贅字
— 每行收尾都要勾著人讀下一行
— 口語自然、用字精準、零推銷感
— 改完附上條列：改了哪裡、為什麼更好
----------------------------------------
📄 內容（Content）= {content}
💬 語氣（Voice）= {voice}
🎯 受眾（Audience）= {audience}""",
        description="改寫草稿，刪除廢話與軟弱句，每行勾著讀下一行，提升停留時間、完讀率、收藏與分享。",
    ),
    5: PromptDefinition(
        id=5,
        key="authority_positioning",
        series="faceless_carousel",
        series_index=5,
        title="不吹噓的個人品牌專業權威改寫",
        role="頂尖個人品牌定位顧問",
        variables=("content", "audience", "brand_voice"),
        template="""扮演一位頂尖個人品牌定位顧問，
專門幫個人 IP 在不吹噓自己的前提下，
建立讓人信服的專業權威。
你的任務：
改寫我提供的內容，
讓它透出實力與份量，同時做到：
— 沒有說教感、沒有大師腔
— 不堆數字、不刻意秀成績
— 不自大、不高高在上
— 讀起來像真正懂行的人在講實話
給我 3 個改寫版本：
版本一：質感版（有餘韻、有留白）
版本二：俐落版（短句、節奏快、有力）
版本三：高級版（字字精準、低調有重量）
每個版本後面，說明它最適合用在哪種場合。
----------------------------------------
📄 內容（Content）= {content}
👥 受眾（Audience）= {audience}
📢 品牌語氣（Brand voice）= {brand_voice}""",
        description="去大師腔、去說教感，改寫為質感版、俐落版、高級版三種懂行者調性。",
    ),
}

# ============================================================================
# Series 2: 短影音爆款與假設驗證體系 (Short-Form Reels Series, ID 06 ~ 12)
# ============================================================================
SHORT_VIDEO_REELS_PROMPTS: dict[int, PromptDefinition] = {
    6: PromptDefinition(
        id=6,
        key="reels_01_topics",
        series="short_video_reels",
        series_index=1,
        title="找出未來 7 天最該拍的題目",
        role="短影音策略顧問",
        variables=("niche", "audience", "followers", "stage_goal"),
        template="""你現在是我的 Instagram Reels 策略顧問。
我的領域是【{niche}】，目標受眾是【{audience}】，目前粉絲數【{followers}】，這階段目標是【{stage_goal}】。

給我 7 個未來 7 天內做得出來的 Reels 題目。

每一題包含：
❶ 受眾的痛點或渴望
❷ 內容切入角度
❸ 開頭鉤子概念
❹ 呈現形式
❺ 觀眾看完帶走什麼
❻ 為什麼這題適合我

排序邏輯：受眾需求強度優先於熱門程度，原創角度優先於跟風題材。""",
        description="鎖定領域與階段目標，產生未來 7 天內做得出來的 7 個高需求原創短影音題目。",
    ),
    7: PromptDefinition(
        id=7,
        key="reels_02_hooks",
        series="short_video_reels",
        series_index=2,
        title="找出最強的開場鉤子",
        role="爆款短影音鉤子文案操盤手",
        variables=("topic", "audience"),
        template="""我這支 Reels 的主題是【{topic}】，受眾是【{audience}】。

寫 20 個專門用在前 1 到 3 秒的開場鉤子。

用不同機制去寫：
製造好奇 ｜ 反差對比 ｜ 點名具體問題 ｜ 指出常見錯誤 ｜ 前後轉變 ｜ 強烈立場 ｜ 敘事張力 ｜ 實用承諾

避開標題黨與空話。

寫完依四個標準排名前 5 名：
語意清楚、好奇程度、與受眾相關性、能否讓對的人繼續看下去。每一名說明上榜理由。""",
        description="產出 20 個前 1~3 秒短影音鉤子，涵蓋 8 大機制，並評選前 5 名與推薦理由。",
    ),
    8: PromptDefinition(
        id=8,
        key="reels_03_script",
        series="short_video_reels",
        series_index=3,
        title="把題目寫成留得住人的短影音腳本",
        role="短影音完播率腳本編導",
        variables=("topic",),
        template="""這是我的 Reels 題目：【{topic}】。把它做成一支以留存率為目標的腳本。

內容包含：
❶ 開場鉤子
❷ 分鏡結構（一鏡一段）
❸ 口播逐字稿
❹ 螢幕字卡
❺ 畫面切換點
❻ 價值交付段
❼ 結尾收法

每一段都要有存在的理由。刪掉廢話，價值早點給，後面接得住時才製造懸念。

標出每一段的大約秒數。語氣像真人講話，不要 AI 腔。""",
        description="產出 7 大要素短影音腳本（分鏡、口播逐字稿、字卡、切鏡、秒數標註、零 AI 腔）。",
    ),
    9: PromptDefinition(
        id=9,
        key="reels_04_save_share",
        series="short_video_reels",
        series_index=4,
        title="讓人想收藏也想傳給朋友",
        role="社群裂變傳播顧問",
        variables=("topic",),
        template="""把【{topic}】做成一支會讓人真心想收藏、或想傳給某個人的 Reels。

從五個角度各給我 1 個概念：
❶ 實用性：現在就能用
❷ 身份認同：這就是我
❸ 情緒相關：戳到心裡
❹ 意外感：跟想像的不一樣
❺ 解決問題：正在卡住的事

每個概念寫出：鉤子、價值結構、畫面概念、自然的行動呼籲。

影片裡不要叫人分享，不要硬做互動，不要誇大承諾。
內容本身要有用到「傳出去像在幫朋友一個忙」的程度。""",
        description="從實用、認同、情緒、意外、解題 5 角度產出具備高轉發與收藏價值概念，無推銷感。",
    ),
    10: PromptDefinition(
        id=10,
        key="reels_05_revival",
        series="short_video_reels",
        series_index=5,
        title="把發過的 Reels 重新救回來",
        role="短影音數據覆盤與改寫顧問",
        variables=("content_and_metrics",),
        template="""我會貼上我的 Reels 內容、腳本、文案與後台數據：
【{content_and_metrics}】。
用現有資訊診斷這支最強和最弱的地方。

分析項目：
鉤子 ｜ 題目 ｜ 表達清晰度 ｜ 節奏 ｜ 留存曲線 ｜ 分享數 ｜ 收藏數 ｜ 留言 ｜ 主頁點擊 ｜ 轉換訊號（有數據的才分析）。

然後告訴我三件事：
❶ 哪些結論可以確定
❷ 哪些是數據看不出來、不能亂猜的
❸ 下一支最該優先改的 3 個地方

最後用這些洞察，把這支 Reels 重寫一次。""",
        description="依後台數據診斷強弱項，明確標示確定結論與不亂猜盲點，輸出 Top 3 改動並重寫腳本。",
    ),
    11: PromptDefinition(
        id=11,
        key="reels_06_trends",
        series="short_video_reels",
        series_index=6,
        title="跟風要跟得有策略（機制 ≠ 影片）",
        role="短影音趨勢策略分析師",
        variables=("trend", "niche"),
        template="""我正在考慮的趨勢或形式是：【{trend}】。
我的領域是【{niche}】。

拆解每一個趨勢背後真正運作的內容機制，
然後告訴我怎麼把那個機制搬到我的受眾身上，
而不用照抄別人的影片。

接著用我的專業、經歷、案例與觀點，
給我 10 個原創延伸概念。

其中只要有任何一個是硬套、已經過度飽和、
或模仿痕跡太重，直接標出來並說明原因。""",
        description="拆解熱門趨勢底層機制並移植到垂直領域，產出 10 個原創概念並標出過度飽和警告。",
    ),
    12: PromptDefinition(
        id=12,
        key="reels_07_matrix",
        series="short_video_reels",
        series_index=7,
        title="排出你的 7 天測試表（假設驗證矩陣）",
        role="短影音成長實驗排程顧問",
        variables=("niche", "goal", "daily_count", "formats"),
        template="""幫我排一張 7 天 Reels 測試計畫，領域是【{niche}】。
我的目標是【{goal}】，每天可以發【{daily_count}】支，
能做的形式有【{formats}】。

每一支標明：
❶ 在驗證什麼假設
❷ 題目
❸ 鉤子
❹ 形式
❺ 觀眾能拿到什麼
❻ 行動呼籲
❼ 要盯的主要指標

七支要刻意拉開差異，讓我測得出哪種題目、哪種鉤子、
哪種形式、哪種角度表現最好。不要七支都在講同一件事
的變形。""",
        description="排出 7 天正交差異化 Reels 測試矩陣，標注假設、形式、鉤子與監控指標。",
    ),
}

# 全體 Prompts 合併字典（統一編號 1 到 12）
PROMPTS: dict[int, PromptDefinition] = {**FACELESS_CAROUSEL_PROMPTS, **SHORT_VIDEO_REELS_PROMPTS}
