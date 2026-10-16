"""Zero-dependency SVG card & carousel generator (1080x1350, 4:5 Instagram format)."""

from __future__ import annotations

import html
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .workflow import WorkflowState


@dataclass
class SlideData:
    title: str
    body_lines: list[str]
    page: int
    total: int
    tag: str = "IG PROMPT FRAMEWORK"
    is_cover: bool = False
    is_cta: bool = False


def _wrap_text(text: str, max_chars: int = 24) -> list[str]:
    """Simple line-wrapping helper for Chinese & English text."""
    lines: list[str] = []
    for raw_line in text.splitlines():
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        while len(raw_line) > max_chars:
            lines.append(raw_line[:max_chars])
            raw_line = raw_line[max_chars:]
        if raw_line:
            lines.append(raw_line)
    return lines


def render_svg_card(slide: SlideData) -> str:
    """Generate a clean, modern, dark-mode SVG card."""
    width = 1080
    height = 1350

    escaped_title = html.escape(slide.title)
    escaped_tag = html.escape(slide.tag.upper())

    # Generate body text spans
    body_spans: list[str] = []
    y_start = 580 if slide.is_cover else 500
    line_height = 54

    for i, line in enumerate(slide.body_lines):
        y = y_start + (i * line_height)
        body_spans.append(
            f'<tspan x="120" y="{y}">{html.escape(line)}</tspan>'
        )
    body_markup = "\n        ".join(body_spans)

    accent_color = "#38bdf8" if slide.is_cover else ("#ec4899" if slide.is_cta else "#818cf8")
    title_size = "64" if slide.is_cover else "52"
    title_y = "450" if slide.is_cover else "380"

    # Pagination markup
    pagination = f"{slide.page} / {slide.total}"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#020617" />
    </linearGradient>
    <linearGradient id="cardGlow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#0f172a" stop-opacity="0.9" />
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" fill="url(#bg)" />

  <!-- Accent top border -->
  <rect x="0" y="0" width="{width}" height="12" fill="{accent_color}" />

  <!-- Card Container -->
  <rect x="60" y="80" width="960" height="1190" rx="36" fill="url(#cardGlow)" stroke="#334155" stroke-width="2" />

  <!-- Header: Tag / Branding -->
  <text x="120" y="180" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="24" font-weight="700" letter-spacing="4" fill="{accent_color}">{escaped_tag}</text>

  <!-- Header: Pagination -->
  <text x="960" y="180" text-anchor="end" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="24" font-weight="600" fill="#64748b">{pagination}</text>

  <!-- Divider -->
  <line x1="120" y1="220" x2="960" y2="220" stroke="#334155" stroke-width="2" />

  <!-- Title -->
  <text x="120" y="{title_y}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="{title_size}" font-weight="800" fill="#f8fafc" letter-spacing="-1">
    {escaped_title}
  </text>

  <!-- Body Content -->
  <text font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="34" font-weight="400" fill="#cbd5e1" line-height="1.6">
    {body_markup}
  </text>

  <!-- Footer CTA / Watermark -->
  <text x="120" y="1200" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="22" font-weight="500" fill="#64748b">
    @SanHsien • IG GROWTH PROMPTS
  </text>
  <text x="960" y="1200" text-anchor="end" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="22" font-weight="600" fill="{accent_color}">
    SWIPE ➔
  </text>
</svg>
"""
    return svg


def generate_carousel_from_workflow(state: WorkflowState, output_dir: str | Path) -> list[Path]:
    """Extract workflow deliverables and render a complete set of carousel SVGs."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    cfg = state.config
    topic = cfg.get("idea", cfg.get("niche", "Instagram 內容成長指南"))
    hook = "越努力日更，演算法越容易放棄你。"

    # Check if Step 2 produced a hook
    s2 = state.steps.get(2)
    if s2 and s2.output:
        for line in s2.output.splitlines():
            if "2. 逆向型：" in line:
                hook = line.split("2. 逆向型：", 1)[1].split("（")[0].strip()
                break

    slides_spec = [
        SlideData(
            title=hook,
            body_lines=[
                "很多創作者卡在「每天發文卻沒人看」。",
                "",
                "問題不在頻率，而在內容結構。",
                "這篇拆解高完讀貼文的 3 大關鍵機制。",
            ],
            page=1,
            total=5,
            is_cover=True,
        ),
        SlideData(
            title="關鍵 1：反套路選題",
            body_lines=[
                "讀者每天看到上百篇流水帳。",
                "",
                "先列出 7 種大家看膩的廢話套路，",
                "主動避開它們，你的內容才具備稀缺性。",
                "新鮮感是手指停住的第一理由。",
            ],
            page=2,
            total=5,
        ),
        SlideData(
            title="關鍵 2：滑梯文案效應",
            body_lines=[
                "每行收尾都要勾著讀者讀下一行。",
                "",
                "• 刪除軟弱句與冗贅修飾詞",
                "• 用具體數據代替空泛保證",
                "• 保留行家講實話的自然節奏",
            ],
            page=3,
            total=5,
        ),
        SlideData(
            title="關鍵 3：不露臉視覺化",
            body_lines=[
                "手邊沒有器材，一樣能做出高觸及：",
                "",
                "• 純字幕短片（節奏快切）",
                "• 4:5 輪播圖卡（高收藏複利）",
                "• 無聲靜態慢動態（聚焦文字）",
            ],
            page=4,
            total=5,
        ),
        SlideData(
            title="結尾行動清單",
            body_lines=[
                "打造個人品牌，不靠運氣靠系統。",
                "",
                "點擊收藏這組卡片，",
                "下次產出內容前逐項對照檢查！",
            ],
            page=5,
            total=5,
            is_cta=True,
        ),
    ]

    generated_files: list[Path] = []
    for s in slides_spec:
        svg_content = render_svg_card(s)
        file_path = out / f"slide_{s.page:02d}.svg"
        file_path.write_text(svg_content, encoding="utf-8")
        generated_files.append(file_path)

    return generated_files
