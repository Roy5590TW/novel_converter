"""
Load and validate raw chapter data from JSON.

Args:
    json_path (str): Path to the JSON file.

Returns:
    list[dict]: A list of chapter objects containing 'title' and 'content'.
"""

import json
from typing import List, Dict


def load_chapter_json(json_path: str) -> List[Dict[str, str]]:
    """Load and validate chapters from JSON file."""
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON format: {exc}") from exc
    except OSError as exc:
        raise OSError(f"Failed to read JSON file: {exc}") from exc

    if not isinstance(data, list):
        raise ValueError("JSON root must be a list of chapter objects.")

    for index, chapter in enumerate(data):
        if not isinstance(chapter, dict):
            raise ValueError(f"Chapter #{index+1} must be an object.")
        if "title" not in chapter or "content" not in chapter:
            raise ValueError(f"Chapter #{index+1} missing required keys.")

    return data
