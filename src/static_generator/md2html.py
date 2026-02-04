#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Minimal static novel generator compatible with official WNSG-style content.

Features:
- Load multiple novels inside content/*
- Parse markdown files with YAML front-matter
- Build chapter pages
- Build novel index pages
- Clean architecture, no external dependencies
"""

import os
import re
import html
from typing import Dict, List, Tuple

# -------------------------------------------------------------
# Utilities
# -------------------------------------------------------------

def read_text(path: str) -> str:
    """Read UTF-8 text safely."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text(path: str, text: str):
    """Write UTF-8 text, ensuring directory exists."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


# -------------------------------------------------------------
# Front Matter Parser
# -------------------------------------------------------------

FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_front_matter(text: str) -> Tuple[Dict, str]:
    """
    Extract YAML front matter and body.

    Returns:
        meta dict, body string
    """
    m = FRONT_RE.match(text)
    if not m:
        return {}, text

    yaml_block = m.group(1)
    body = text[m.end():]

    try:
        # Python built-in YAML is not available,
        # but we can fake simple key: value pairs.
        meta = {}
        for line in yaml_block.splitlines():
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    except Exception:
        meta = {}

    return meta, body


# -------------------------------------------------------------
# Data structures
# -------------------------------------------------------------

class Chapter:
    """Represents a chapter parsed from markdown."""

    def __init__(self, cid: str, title: str, body: str, meta: Dict):
        self.id = cid
        self.title = title
        self.body = body
        self.meta = meta


class Novel:
    """Represents a single novel."""

    def __init__(self, slug: str, title: str, author: str, description: str):
        self.slug = slug
        self.title = title
        self.author = author
        self.description = description
        self.chapters: List[Chapter] = []


# -------------------------------------------------------------
# Loaders
# -------------------------------------------------------------

def load_novel_config(path: str) -> Dict:
    """
    Read config.yaml (simple key: value format).
    """
    raw = read_text(path)

    cfg = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        cfg[k.strip()] = v.strip().strip('"')

    return cfg


def load_chapters(chapter_dir: str) -> List[Chapter]:
    """
    Load markdown chapters with front matter.
    """

    files = sorted(f for f in os.listdir(chapter_dir) if f.endswith(".md"))
    chapters: List[Chapter] = []

    for fn in files:
        path = os.path.join(chapter_dir, fn)
        raw = read_text(path)

        meta, body = parse_front_matter(raw)

        cid = str(meta.get("chapter", fn.replace(".md", "")))
        title = meta.get("title", f"Chapter {cid}")

        published = meta.get("published", "true").lower()
        if published in ("false", "0", "no"):
            continue

        chapters.append(Chapter(cid=cid, title=title, body=body, meta=meta))

    chapters.sort(key=lambda c: int(c.id))
    return chapters


def load_novels(content_dir: str) -> List[Novel]:
    """
    Load all novels inside content/*.
    """

    novels: List[Novel] = []

    for slug in os.listdir(content_dir):
        novel_dir = os.path.join(content_dir, slug)
        if not os.path.isdir(novel_dir):
            continue

        config_path = os.path.join(novel_dir, "config.yaml")
        chapters_dir = os.path.join(novel_dir, "chapters")

        if not os.path.exists(config_path) or not os.path.exists(chapters_dir):
            continue

        cfg = load_novel_config(config_path)

        novel = Novel(
            slug=slug,
            title=cfg.get("title", slug),
            author=cfg.get("author", ""),
            description=cfg.get("description", "")
        )

        novel.chapters = load_chapters(chapters_dir)

        if not novel.chapters:
            continue

        novels.append(novel)

    # sort novels by title
    novels.sort(key=lambda n: n.title.lower())
    return novels


# -------------------------------------------------------------
# Rendering
# -------------------------------------------------------------

BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="utf-8">

    <!-- Lock zoom -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

    <title>{title}</title>

    <style>

        /* ---------- Light / Dark theme variables ---------- */
        :root {{
            --bg-page: #eeeeee;
            --bg-paper: #fffdf8;
            --text: #222222;
            --link: #4a6fa5;
        }}

        body.dark {{
            --bg-page: #1a1a1a;
            --bg-paper: #222222;
            --text: #e6e6e6;
            --link: #7aa2d6;
        }}

        /* ---------- Layout ---------- */
        body {{
            background: var(--bg-page);
            margin: 0;
            display: flex;
            justify-content: center;
            font-family: "Noto Serif TC", "Times New Roman", serif;

            transition: background 0.3s ease;
        }}

        .reader {{
            width: 800px;
            max-width: 95vw;

            background: var(--bg-paper);
            margin: 40px 0;

            padding: 60px;

            font-size: 26px;     /* big comfortable text */
            line-height: 2.3;

            color: var(--text);

            box-shadow: 0 6px 25px rgba(0,0,0,0.2);

            overflow-y: auto;

            transition: background 0.3s ease, color 0.3s ease;
        }}

        h1 {{
            margin-top: 0;
            font-size: 42px;
        }}

        a {{
            color: var(--link);
            text-decoration: none;
        }}

        .nav {{
            margin-top: 40px;
            font-size: 20px;
        }}

        /* -------- Dark mode button -------- */
        .toggle {{
            position: fixed;
            top: 12px;
            right: 12px;

            padding: 8px 14px;

            background: #444;
            color: #fff;

            border-radius: 6px;
            cursor: pointer;

            font-size: 14px;

            z-index: 9999;

            transition: background 0.25s ease;
        }}

        body.dark .toggle {{
            background: #bbb;
            color: #000;
        }}

    </style>

    <script>
        function toggleTheme() {{
            document.body.classList.toggle("dark");

            // persist preference
            if (document.body.classList.contains("dark")) {{
                localStorage.setItem("reader-theme", "dark");
            }} else {{
                localStorage.setItem("reader-theme", "light");
            }}
        }}

        // load theme
        window.addEventListener("DOMContentLoaded", () => {{
            const saved = localStorage.getItem("reader-theme");
            if (saved === "dark") {{
                document.body.classList.add("dark");
            }}
        }});
    </script>
</head>

<body>

    <div class="toggle" onclick="toggleTheme()">🌓 切換模式</div>

    <div class="reader">
        {content}
    </div>

</body>
</html>
"""






def render_chapter_page(novel: Novel, chapter: Chapter) -> str:
    """Render a single chapter page with navigation buttons."""

    # Escape text safely
    body = html.escape(chapter.body).replace("\n", "<br>")

    # Locate prev / next chapters
    idx = novel.chapters.index(chapter)

    prev_link = None
    next_link = None

    if idx > 0:
        prev_ch = novel.chapters[idx - 1]
        prev_link = f"{prev_ch.id}.html"

    if idx < len(novel.chapters) - 1:
        next_ch = novel.chapters[idx + 1]
        next_link = f"{next_ch.id}.html"

    # Navigation button block
    nav_buttons = "<div style='margin-top:20px;'>"

    if prev_link:
        nav_buttons += f"<a href='{prev_link}'>⬅ Previous</a> &nbsp;&nbsp;"

    nav_buttons += "<a href='../index.html'>📚 Back to list</a>"

    if next_link:
        nav_buttons += f"&nbsp;&nbsp; <a href='{next_link}'>Next ➡</a>"

    nav_buttons += "</div>"

    content = f"""
    <h1>{html.escape(chapter.title)}</h1>
    <p><em>{html.escape(novel.title)} — {html.escape(novel.author)}</em></p>

    <div class="chapter">{body}</div>

    {nav_buttons}
    """

    return BASE_TEMPLATE.format(title=chapter.title, content=content)



def render_novel_index(novel: Novel) -> str:
    """Render the novel's chapter list."""

    items = []
    for ch in novel.chapters:
        items.append(f'<li><a href="chapters/{ch.id}.html">{html.escape(ch.title)}</a></li>')

    chapters_html = "<ul>\n" + "\n".join(items) + "\n</ul>"

    content = f"""
    <h1>{html.escape(novel.title)}</h1>
    <p>Author: {html.escape(novel.author)}</p>
    <p>{html.escape(novel.description)}</p>

    <h2>Chapters</h2>
    {chapters_html}

    <p><a href="../index.html">Back to library</a></p>
    """

    return BASE_TEMPLATE.format(title=novel.title, content=content)


def render_library_index(novels: List[Novel]) -> str:
    """Render index listing all novels."""

    items = []
    for n in novels:
        items.append(f'<li><a href="{n.slug}/index.html">{html.escape(n.title)}</a></li>')

    html_list = "<ul>\n" + "\n".join(items) + "\n</ul>"

    content = f"""
    <h1>Novel Library</h1>
    {html_list}
    """

    return BASE_TEMPLATE.format(title="Library", content=content)


# -------------------------------------------------------------
# Builder
# -------------------------------------------------------------

def build_site(content_dir: str, out_dir: str):
    """Build entire static site."""

    novels = load_novels(content_dir)

    os.makedirs(out_dir, exist_ok=True)

    # library index
    write_text(os.path.join(out_dir, "index.html"), render_library_index(novels))

    for novel in novels:
        novel_out = os.path.join(out_dir, novel.slug)
        chapters_out = os.path.join(novel_out, "chapters")

        write_text(os.path.join(novel_out, "index.html"), render_novel_index(novel))

        for ch in novel.chapters:
            page = render_chapter_page(novel, ch)
            write_text(os.path.join(chapters_out, f"{ch.id}.html"), page)

    print(f"Built {len(novels)} novels → {out_dir}")


# -------------------------------------------------------------
# Main
# -------------------------------------------------------------

if __name__ == "__main__":
    CONTENT = "content"
    OUTPUT = "output"

    build_site(CONTENT, OUTPUT)
