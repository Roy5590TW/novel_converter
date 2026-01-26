"""
Normalize title and content text for safe Markdown output.

Returns:
    tuple[str, str]: (normalized_title, normalized_content)
"""

def normalize_title(title: str) -> str:
    """Normalize title by removing line breaks and extra whitespace."""
    if not isinstance(title, str):
        raise ValueError("Title must be a string.")

    # Remove CRLF/LF and collapse into one line
    cleaned = " ".join(title.replace("\r", "").replace("\n", " ").split())
    return cleaned


def normalize_content(content: str) -> str:
    """Normalize content newlines but preserve all readable formatting."""
    if not isinstance(content, str):
        raise ValueError("Content must be a string.")

    # Convert CRLF and CR → LF
    text = content.replace("\r\n", "\n").replace("\r", "\n")
    return text
