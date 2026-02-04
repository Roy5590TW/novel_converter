"""
Write Markdown chapter files to structured directories.

Args:
    base_dir (str): Output root directory.
    novel_key (str): Novel identifier in English.
    index (int): Chapter index.
    markdown (str): Full markdown content.
"""

import os


def write_chapter(base_dir: str, novel_key: str, index: int, markdown: str) -> str:
    """Write a chapter markdown file and return its path."""
    chapter_id = str(index).zfill(4)
    output_path = os.path.join(base_dir, novel_key, "chapters")

    try:
        os.makedirs(output_path, exist_ok=True)
    except OSError as exc:
        raise OSError(f"Failed to create output directory: {exc}") from exc

    file_path = os.path.join(output_path, f"{chapter_id}.md")

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(markdown)
    except OSError as exc:
        raise IOError(f"Failed to write file: {exc}") from exc

    return file_path


def write_config_yaml(base_dir: str, novel_key: str) -> str:
    """
    Write a config.yaml file for the novel if it does not already exist.
    Returns the path to the config file.
    """
    novel_dir = os.path.join(base_dir, novel_key)
    os.makedirs(novel_dir, exist_ok=True) # Ensure novel directory exists

    config_path = os.path.join(novel_dir, "config.yaml")

    if not os.path.exists(config_path):
        template_content = (
            'title: "title"\n'
            'author: "author"\n'
            'description: "description."\n'
        )
        try:
            with open(config_path, "w", encoding="utf-8") as file:
                file.write(template_content)
        except OSError as exc:
            raise IOError(f"Failed to write config.yaml: {exc}") from exc
    
    return config_path
