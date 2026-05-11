import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN, USE_PROXY, PROXY_URL
from handlers import commands, idcollector
from database.manager import DBManager
from middlewares.i18n import L10nMiddleware


async def main():
    logging.basicConfig(level=logging.INFO)

    session = AiohttpSession(proxy=PROXY_URL) if USE_PROXY and PROXY_URL else None
    bot = Bot(token=BOT_TOKEN, session=session, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()
    db = DBManager()

    await db.connect()

    dp.update.outer_middleware(L10nMiddleware(db))
    dp.include_routers(commands.router, idcollector.router)

    try:
        await dp.start_polling(bot)
    finally:
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
