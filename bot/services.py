from pathlib import Path
from aiogram import Bot
from aiogram.types import FSInputFile
from bot.config import get_settings

async def show_page(target, text, reply_markup=None, photo: str|None=None):
    s=get_settings(); photo = photo or s.default_cover_path
    if hasattr(target, 'message'):
        msg=target.message
        try:
            if Path(photo).exists():
                await msg.delete()
                return await msg.answer_photo(FSInputFile(photo), caption=text, reply_markup=reply_markup)
            return await msg.edit_text(text, reply_markup=reply_markup)
        except Exception:
            try: return await msg.answer(text, reply_markup=reply_markup)
            except Exception: pass
    else:
        if Path(photo).exists(): return await target.answer_photo(FSInputFile(photo), caption=text, reply_markup=reply_markup)
        return await target.answer(text, reply_markup=reply_markup)
