import aiosqlite
from pathlib import Path

DB_PATH = Path("data/novels.db")

def get_db():
    return aiosqlite.connect(DB_PATH)

async def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    async with get_db() as db:
        db.row_factory = aiosqlite.Row
        await db.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_name TEXT UNIQUE NOT NULL
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS book_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER UNIQUE NOT NULL,
                author TEXT DEFAULT '未知',
                tags TEXT DEFAULT '',
                status TEXT DEFAULT '連載中',
                description TEXT DEFAULT '暫無簡介',
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE
            )
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS chapters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                chapter_num INTEGER,
                title TEXT,
                content TEXT,
                FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE,
                UNIQUE(book_id, chapter_num)
            )
        ''')

        await db.commit()