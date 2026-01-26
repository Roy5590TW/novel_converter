"""
Convert normalized chapter data into Markdown text with front-matter.

Args:
    title (str): Normalized chapter title.
    chapter_num (int): Chapter index (starting from 1).
    content (str): Normalized chapter content.

Returns:
    str: Full markdown text including YAML front-matter.
"""

def build_markdown(title: str, chapter_num: int, content: str) -> str:
    """Construct markdown text with YAML front-matter."""
    front_matter = (
        "---\n"
        f'title: "{title}"\n'
        f"chapter: {chapter_num}\n"
        "lang: zh-TW\n"
        "published: true\n"
        "tags: []\n"
        "---\n\n"
    )

    return front_matter + content
