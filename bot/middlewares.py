from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from bot.database import SessionLocal
from bot.config import get_settings
from bot.repo import upsert_user

class DbUserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        tg_user = getattr(event, 'from_user', None)
        async with SessionLocal() as s:
            data['session']=s
            if tg_user:
                dbu=await upsert_user(s, tg_user, get_settings().admin_ids)
                data['db_user']=dbu
                if dbu.is_blocked:
                    if isinstance(event, CallbackQuery): await event.answer('⛔ Доступ ограничен', show_alert=True)
                    elif isinstance(event, Message): await event.answer('<b>⛔ Доступ ограничен</b>\n<i>Вы не можете пользоваться ботом.</i>')
                    return
            return await handler(event, data)
