"""Zero-dependency SVG carousel renderer (1080x1350, Instagram 4:5).

Slide content always comes from a slide spec (AI output or a user file).
Nothing is hard-coded: if no spec is found, rendering fails loudly.

Slide spec format (Markdown, slides separated by a line with only ``---``)::

    # Cover title
    body line
    body line

    ---

    # Second slide title
    body line

Inside an AI answer the spec must be wrapped in a fenced block tagged ``slides``.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path

WIDTH = 1080
HEIGHT = 1350
MAX_BODY_LINES = 12
WRAP_WIDTH = 30  # display columns; CJK characters count as 2

SLIDES_FORMAT_ADDENDUM = """【自動化輸出格式（給排版程式讀取）】
在回答最後，把「版本一：輪播貼文」每一張的畫面文字，用下面格式放進一個標記為 slides 的程式碼區塊：
```slides
# 第一張標題
內文一行
---
# 第二張標題
內文一行
```
每張以「# 標題」開頭，張與張之間用單獨一行 --- 分隔，只放畫面上要出現的字。"""

_FENCE_RE = re.compile(r"```slides[ \t]*\r?\n(.*?)\r?\n```", re.DOTALL)
_SEPARATOR_RE = re.compile(r"^\s*---\s*$", re.MULTILINE)


class SlideSpecError(ValueError):
    """Raised when no usable slide spec is available."""


@dataclass
class SlideData:
    title: str
    body_lines: list[str]
    page: int
    total: int
    tag: str = "IG GROWTH PROMPTS"

    @property
    def is_cover(self) -> bool:
        return self.page == 1

    @property
    def is_last(self) -> bool:
        return self.page == self.total


def _display_width(ch: str) -> int:
    return 2 if ord(ch) > 0x2E7F else 1


def wrap_line(text: str, width: int = WRAP_WIDTH) -> list[str]:
    """Wrap by display width so mixed CJK and Latin text stays inside the card."""
    lines: list[str] = []
    current = ""
    used = 0
    for ch in text:
        w = _display_width(ch)
        if used + w > width and current:
            lines.append(current.rstrip())
            current, used = "", 0
            if ch == " ":
                continue
        current += ch
        used += w
    if current.strip():
        lines.append(current.rstrip())
    return lines


def extract_slides_block(answer: str) -> str | None:
    """Return the content of the first ```slides fenced block, if any."""
    match = _FENCE_RE.search(answer or "")
    return match.group(1) if match else None


def parse_slide_spec(spec: str, tag: str = "IG GROWTH PROMPTS") -> list[SlideData]:
    """Parse the slide spec format into SlideData objects."""
    chunks = [c.strip() for c in _SEPARATOR_RE.split(spec or "") if c.strip()]
    parsed: list[tuple[str, list[str]]] = []
    for idx, chunk in enumerate(chunks, start=1):
        raw_lines = [ln.rstrip() for ln in chunk.splitlines()]
        title_idx = next((i for i, ln in enumerate(raw_lines) if ln.lstrip().startswith("#")), None)
        if title_idx is None:
            raise SlideSpecError(f"Slide {idx} has no '# title' line.")
        title = raw_lines[title_idx].lstrip().lstrip("#").strip()
        if not title:
            raise SlideSpecError(f"Slide {idx} has an empty title.")
        body: list[str] = []
        for i, ln in enumerate(raw_lines):
            if i == title_idx:
                continue
            body.extend(wrap_line(ln.strip()) if ln.strip() else [""])
        while body and not body[0]:
            body.pop(0)
        while body and not body[-1]:
            body.pop()
        if len(body) > MAX_BODY_LINES:
            raise SlideSpecError(
                f"Slide {idx} has {len(body)} body lines after wrapping; the limit is {MAX_BODY_LINES}."
            )
        parsed.append((title, body))

    if not parsed:
        raise SlideSpecError("Slide spec is empty.")
    total = len(parsed)
    return [
        SlideData(title=t, body_lines=b, page=i, total=total, tag=tag)
        for i, (t, b) in enumerate(parsed, start=1)
    ]


def render_svg_card(slide: SlideData) -> str:
    """Render one dark-mode SVG card."""
    font = "Inter, 'Noto Sans TC', 'Microsoft JhengHei', -apple-system, 'Segoe UI', Roboto, sans-serif"
    accent = "#38bdf8" if slide.is_cover else ("#ec4899" if slide.is_last else "#818cf8")
    title_lines = wrap_line(slide.title, 18 if slide.is_cover else 22)
    title_size = 64 if slide.is_cover else 52
    title_y = 360 if slide.is_cover else 320

    title_spans = "\n    ".join(
        f'<tspan x="120" y="{title_y + i * (title_size + 16)}">{html.escape(t)}</tspan>'
        for i, t in enumerate(title_lines)
    )
    body_y = title_y + len(title_lines) * (title_size + 16) + 60
    body_spans = "\n    ".join(
        f'<tspan x="120" y="{body_y + i * 56}">{html.escape(line)}</tspan>'
        for i, line in enumerate(slide.body_lines)
        if line
    )
    footer_right = "SWIPE ➔" if not slide.is_last else "SAVE ✦"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#020617" />
    </linearGradient>
  </defs>
  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)" />
  <rect x="0" y="0" width="{WIDTH}" height="12" fill="{accent}" />
  <rect x="60" y="80" width="960" height="1190" rx="36" fill="#1e293b" fill-opacity="0.75" stroke="#334155" stroke-width="2" />
  <text x="120" y="180" font-family="{font}" font-size="24" font-weight="700" letter-spacing="4" fill="{accent}">{html.escape(slide.tag.upper())}</text>
  <text x="960" y="180" text-anchor="end" font-family="{font}" font-size="24" font-weight="600" fill="#64748b">{slide.page} / {slide.total}</text>
  <line x1="120" y1="220" x2="960" y2="220" stroke="#334155" stroke-width="2" />
  <text font-family="{font}" font-size="{title_size}" font-weight="800" fill="#f8fafc">
    {title_spans}
  </text>
  <text font-family="{font}" font-size="34" font-weight="400" fill="#cbd5e1">
    {body_spans}
  </text>
  <text x="960" y="1200" text-anchor="end" font-family="{font}" font-size="22" font-weight="600" fill="{accent}">{footer_right}</text>
</svg>
"""


def render_slides(slides: list[SlideData], output_dir: str | Path) -> list[Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    for s in slides:
        path = out / f"slide_{s.page:02d}.svg"
        path.write_text(render_svg_card(s), encoding="utf-8")
        files.append(path)
    return files


def render_slides_from_spec_file(spec_path: str | Path, output_dir: str | Path) -> list[Path]:
    text = Path(spec_path).read_text(encoding="utf-8")
    block = extract_slides_block(text)
    return render_slides(parse_slide_spec(block if block is not None else text), output_dir)


def render_slides_from_answer(answer: str, output_dir: str | Path) -> list[Path]:
    """Render from an AI answer. Raise SlideSpecError when the answer has no slides block."""
    block = extract_slides_block(answer)
    if block is None:
        raise SlideSpecError("The answer has no ```slides block.")
    return render_slides(parse_slide_spec(block), output_dir)
