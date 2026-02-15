import json
from pathlib import Path
from .database import get_db

INPUTS_DIR = Path("inputs")

async def run_import():
    async with get_db() as db:
        for json_file in INPUTS_DIR.glob("*.json"):
            book_name = json_file.stem
            
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            chapters_to_db = [
                (book_name, i + 1, item['title'], item['content']) 
                for i, item in enumerate(data)
            ]
            
            await db.executemany(
                "INSERT OR IGNORE INTO chapters (book_name, chapter_num, title, content) VALUES (?, ?, ?, ?)",
                chapters_to_db
            )
            print(f"-> 處理完成: {book_name} (共 {len(chapters_to_db)} 章)")
            
        await db.commit()