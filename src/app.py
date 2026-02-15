from fastapi import APIRouter, HTTPException
from .database import get_db

router = APIRouter()

@router.get("/api/books")
async def get_books():
    async with get_db() as db:
        db.row_factory = None
        async with db.execute("SELECT book_name FROM books") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

@router.get("/api/chapters/{book_name}")
async def get_chapters(book_name: str):
    async with get_db() as db:
        db.row_factory = None
        sql = """
            SELECT c.chapter_num, c.title 
            FROM chapters c
            JOIN books b ON c.book_id = b.id
            WHERE b.book_name = ?
            ORDER BY c.chapter_num
        """
        async with db.execute(sql, (book_name,)) as cursor:
            rows = await cursor.fetchall()
            if not rows:
                raise HTTPException(status_code=404, detail="找不到這本書")
            return [{"chapter_num": r[0], "title": r[1]} for r in rows]

@router.get("/api/content/{book_name}/{ch_num}")
async def get_content(book_name: str, ch_num: int):
    async with get_db() as db:
        db.row_factory = None
        sql = """
            SELECT c.title, c.content 
            FROM chapters c
            JOIN books b ON c.book_id = b.id
            WHERE b.book_name = ? AND c.chapter_num = ?
        """
        async with db.execute(sql, (book_name, ch_num)) as cursor:
            row = await cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="找不到該章節")
            return {"title": row[0], "content": row[1]}