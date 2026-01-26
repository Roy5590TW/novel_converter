"""
Main orchestrator for converting JSON chapter data into Markdown files.

Usage:
    python main.py --input chapters.json --output content --novel-key my-novel
"""

import argparse

from loader import load_chapter_json
from normalizer import normalize_title, normalize_content
from formatter import build_markdown
from writer import write_chapter


def run_converter(input_path: str, output_path: str, novel_key: str) -> None:
    """Execute conversion process from JSON to markdown files."""
    chapters = load_chapter_json(input_path)

    for index, chapter in enumerate(chapters, start=1):
        raw_title = chapter["title"]
        raw_content = chapter["content"]

        title = normalize_title(raw_title)
        content = normalize_content(raw_content)

        md_text = build_markdown(title, index, content)
        file_path = write_chapter(output_path, novel_key, index, md_text)

        print(f"[OK] Chapter {index} -> {file_path}")


def main() -> None:
    """Parse arguments and start converter."""
    parser = argparse.ArgumentParser(description="JSON → Markdown chapter converter")
    parser.add_argument("--input", required=True, help="Path to JSON file")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--novel-key", required=True, help="Novel key (English only)")

    args = parser.parse_args()

    run_converter(args.input, args.output, args.novel_key)


if __name__ == "__main__":
    main()
