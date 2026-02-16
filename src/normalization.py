import re
from .logger_config import logger


def normalize_chapter_title(title: str, ch_num: int, content: str) -> str:
    title = title.strip()
    char_count = len(content.strip())
    
    # --- 1. Header Normalization ---
    head_pattern = r'^(第?[0-9一二三四五六七八九十百千萬]+[卷冊部].*?第[0-9一二三四五六七八九十百千萬]+[章回]|第[0-9一二三四五六七八九十百千萬]+[章回])'
    if not re.search(head_pattern, title):
        title = f"第 {ch_num} 章 - {title}"
    
    is_pure_digit = re.match(r'^\d+$', title)
    if re.search(head_pattern, title):
        pass
    elif is_pure_digit:
        title = f"第 {title} 章"
    else:
        if not re.search(r'第[0-9一二三四五六七八九十百千萬]+[章回]', title):
            title = f"第 {ch_num} 章 - {title}"
        else:
            logger.info(f"Detected potential chapter pattern in title: '{title}', skipping prefix.")

    # --- 2. Footer Normalization ---
    title = re.sub(r'[(\[（【]\d+\s?字[)\]）】]$', '', title).strip()
    tail_pattern = r'[(\[（【][^()\[\]（）【]*\d+\s?字[^()\[\]（）【]*[)\]）】]$|字數[:：]\d+'
    if not re.search(tail_pattern, title):
        title = f"{title} ({char_count}字)"
    
    return title