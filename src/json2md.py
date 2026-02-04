"""
Orchestrates the conversion of JSON chapter data into Markdown files.

This script takes a JSON input file, generates a unique novel key,
creates/updates a config.yaml, and converts the JSON content into
structured Markdown chapter files.

Usage:
    python src/json2md.py --input <path_to_json_file>
"""

import argparse
import secrets
import string

from .loader import load_chapter_json
from .normalizer import normalize_title, normalize_content
from .formatter import build_markdown
from .writer import write_chapter, write_config_yaml


def run_converter(input_path: str, output_path: str, novel_key: str) -> None:
    """Execute conversion process from JSON to markdown files."""
    write_config_yaml(output_path, novel_key) # Call the new function
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

    args = parser.parse_args()

    # Generate a random 32-character novel key
    alphabet = string.ascii_letters + string.digits
    novel_key = "".join(secrets.choice(alphabet) for _ in range(32))

    run_converter(args.input, "content", novel_key)


if __name__ == "__main__":
    main()