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
import json
import os

from .loader import load_chapter_json
from .normalizer import normalize_title, normalize_content
from .formatter import build_markdown
from .writer import write_chapter, write_config_yaml

MAPPING_FILE = "content/processed_mapping.json"

def load_mapping() -> dict:
    """Loads the processed files mapping from a JSON file."""
    if not os.path.exists(MAPPING_FILE):
        return {}
    try:
        with open(MAPPING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {} # Return empty if file is corrupt

def save_mapping(mapping: dict) -> None:
    """Saves the processed files mapping to a JSON file."""
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=4)


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

    mapping = load_mapping()
    input_file_basename = os.path.basename(args.input)

    if input_file_basename in mapping:
        novel_key = mapping[input_file_basename]
        print(f"Skipping processing for {input_file_basename}. Using existing novel key: {novel_key}")
        # We still need to run the converter to ensure config.yaml and existing MD files are up-to-date
        # Even if we skip regeneration, the file might have been updated.
        # The writer.py functions handle overwriting existing files.
        run_converter(args.input, "content", novel_key)
    else:
        # Generate a random 32-character novel key
        alphabet = string.ascii_letters + string.digits
        novel_key = "".join(secrets.choice(alphabet) for _ in range(32))
        run_converter(args.input, "content", novel_key)
        mapping[input_file_basename] = novel_key
        save_mapping(mapping)


if __name__ == "__main__":
    main()