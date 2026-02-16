import re
from .logger_config import logger


def normalize_chapter_title(title: str, ch_num: int, content: str) -> str:
    title = title.strip()
    char_count = len(content.strip())
    
    # --- 1. Header Normalization ---
    has_index_pattern = r'^(第?[0-9一二三四五六七八九十百千萬]+[章回節卷冊部]|^[0-9]+$)'
    if re.search(has_index_pattern, title):
        if re.match(r'^[0-9]+$', title):
            title = f"第 {title} 章"
        else:
            pass
    else:
            if f"第 {ch_num} 章" not in title:
                title = f"第 {ch_num} 章 - {title}"
    
    title = re.sub(r'^(第\s?\d+\s?章\s?-\s?){2,}', r'\1', title)
    
    title = re.sub(r'^第\s?(\d+)\s?章\s?-\s?\1$', r'第 \1 章', title)
    title = re.sub(r'^第\s?(\d+)\s?章\s?-\s?\1\s?-\s?', r'第 \1 章 - ', title)

    # --- 2. Footer Normalization ---

    title = re.sub(r'\s?[\(（【\[]\d+\s?字[\)）】\]]$', '', title)
    title = f"{title} ({char_count}字)"
    
    return title