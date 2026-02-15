import re

def normalize_chapter_title(title: str, ch_num: int, content: str) -> str:
    char_count = len(content.strip())
    
    # --- 1. Header Normalization ---
    head_pattern = r'^(第[0-9一二三四五六七八九十百千萬]+[章回]|第?[0-9一二三四五六七八九十百千萬]+[、\s])'
    if not re.search(head_pattern, title):
        title = f"第 {ch_num} 章 - {title}"
    
    # --- 2. Footer Normalization ---
    tail_pattern = r'[(\[（【][^()\[\]（）【]*\d+\s?字[^()\[\]（）【]*[)\]）】]$|字數[:：]\d+'
    if not re.search(tail_pattern, title):
        title = f"{title} ({char_count}字)"
    
    return title