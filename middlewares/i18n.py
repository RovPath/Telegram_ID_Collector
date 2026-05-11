from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from database.manager import DBManager


class L10nMiddleware(BaseMiddleware):
    def __init__(self, db: DBManager):
        self.db = db
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user:
            data["lang"] = await self.db.get_lang(user.id)
            data["db"] = self.db
        return await handler(event, data)
