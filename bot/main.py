import asyncio, logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from bot.config import get_settings
from bot.database import init_db
from bot.middlewares import DbUserMiddleware
from bot.routers import start, catalog, converter, submissions, donations, support, admin

async def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    s=get_settings(); await init_db()
    bot=Bot(s.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp=Dispatcher(storage=MemoryStorage())
    dp.message.middleware(DbUserMiddleware()); dp.callback_query.middleware(DbUserMiddleware())
    for r in [start.router, admin.router, catalog.router, converter.router, submissions.router, donations.router, support.router]: dp.include_router(r)
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info('ScriptBot started')
    await dp.start_polling(bot)

if __name__=='__main__': asyncio.run(main())
