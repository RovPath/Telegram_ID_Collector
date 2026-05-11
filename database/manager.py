import aiosqlite
from typing import Optional
from config import DB_PATH


class DBManager:
    def __init__(self):
        self.path = DB_PATH
        self._db: Optional[aiosqlite.Connection] = None

    async def connect(self):
        if not self._db:
            self._db = await aiosqlite.connect(self.path)
            await self._db.execute(
                "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, lang TEXT DEFAULT 'en')"
            )
            await self._db.commit()

    async def close(self):
        if self._db:
            await self._db.close()

    async def get_lang(self, user_id: int) -> str:
        async with self._db.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else "en"

    async def set_lang(self, user_id: int, lang: str):
        await self._db.execute("INSERT OR REPLACE INTO users (user_id, lang) VALUES (?, ?)", (user_id, lang))
        await self._db.commit()
