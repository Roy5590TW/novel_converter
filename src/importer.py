import json
from pathlib import Path
import asyncio
import aiosqlite
from .database import get_db

INPUTS_DIR = Path("inputs")

async def run_import():
    async with get_db() as db:
        db.row_factory = aiosqlite.Row
        for json_file in INPUTS_DIR.glob("*.json"):
            book_name = json_file.stem
            
            await db.execute("INSERT OR IGNORE INTO books (book_name) VALUES (?)", (book_name,))
            await db.commit()

            async with db.execute("SELECT id FROM books WHERE book_name = ?", (book_name,)) as cursor:
                row = await cursor.fetchone()
                
                if row is None:
                    print(f"警告：無法取得 {book_name} 的 ID，跳過此書。")
                    continue
                
                book_id = row["id"]

            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            chapters_to_db = [
                (book_id, i + 1, item['title'], item['content']) 
                for i, item in enumerate(data)
            ]

            await db.executemany(
                "INSERT OR IGNORE INTO chapters (book_id, chapter_num, title, content) VALUES (?, ?, ?, ?)",
                chapters_to_db
            )
        await db.commit()