"""Prompt definitions and structured metadata."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PromptDefinition:
    id: int
    key: str
    title: str
    role: str
    variables: tuple[str, ...]
    template: str
    description: str


PROMPTS: dict[int, PromptDefinition] = {
    1: PromptDefinition(
        id=1,
        key="niche_ideation",
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
