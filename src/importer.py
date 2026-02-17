import aiosqlite
import json
from pathlib import Path
from .database import get_db
from .normalization import normalize_chapter_title
from .logger_config import logger

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
                    logger.warning(f"警告：無法取得 {book_name} 的 ID，跳過此書。")
                    continue
                book_id = row["id"]

            with open(json_file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)

            metadata_to_db = {
                "author": "未知",
                "tags": "",
                "status": "連載中",
                "description": "暫無簡介"
            }
            chapter_list = []

            for item in raw_data:
                if "metadata" in item:
                    m = item["metadata"]
                    metadata_to_db["author"] = m.get("author", metadata_to_db["author"])
                    metadata_to_db["tags"] = m.get("tags", m.get("sort", metadata_to_db["tags"]))
                    metadata_to_db["status"] = m.get("status", metadata_to_db["status"])
                    metadata_to_db["description"] = m.get("description", m.get("簡介", metadata_to_db["description"]))
                elif "title" in item:
                    chapter_list.append(item)

            await db.execute('''
                INSERT OR REPLACE INTO book_metadata (book_id, author, tags, status, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                book_id, 
                metadata_to_db["author"], 
                metadata_to_db["tags"], 
                metadata_to_db["status"], 
                metadata_to_db["description"]
            ))
            
            chapters_to_db = [
                (
                    book_id, 
                    i + 1, 
                    normalize_chapter_title(item['title'], i + 1, item['content']),
                    item['content']
                ) 
                for i, item in enumerate(chapter_list)
            ]
            if chapters_to_db:
                await db.executemany(
                    "INSERT OR IGNORE INTO chapters (book_id, chapter_num, title, content) VALUES (?, ?, ?, ?)",
                    chapters_to_db
                )
            
            logger.info(f"成功匯入書籍：{book_name}，共 {len(chapters_to_db)} 章。")
            
        await db.commit()