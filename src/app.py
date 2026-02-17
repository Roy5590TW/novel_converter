from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from .database import get_db

router = APIRouter()
favicon_path = 'favicon.ico'

@router.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

@router.get("/api/books")
async def get_books():
    async with get_db() as db:
        db.row_factory = None
        sql = """
            SELECT 
                b.book_name, 
                m.author, 
                m.tags, 
                m.status, 
                m.description
            FROM books b
            LEFT JOIN book_metadata m ON b.id = m.book_id
        """
        async with db.execute(sql) as cursor:
            rows = await cursor.fetchall()
            return [
                {
                    "book_name": r[0],
                    "author": r[1] or "未知",
                    "tags": r[2] or "",
                    "status": r[3] or "連載中",
                    "description": r[4] or "暫無簡介"
                } for r in rows
            ]

@router.get("/api/metadata/{book_name}")
async def get_book_metadata(book_name: str):
    async with get_db() as db:
        db.row_factory = None
        sql = """
            SELECT m.author, m.tags, m.status, m.description
            FROM book_metadata m
            JOIN books b ON m.book_id = b.id
            WHERE b.book_name = ?
        """
        async with db.execute(sql, (book_name,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="找不到該書的元數據")
            return {
                "author": row[0],
                "tags": row[1],
                "status": row[2],
                "description": row[3]
            }

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