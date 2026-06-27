from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from bot.callbacks import CatalogCb
from bot.database import Submission
from bot.config import get_settings
from bot.keyboards import back_home
router=Router()

@router.callback_query(CatalogCb.filter(F.action=='submit'))
async def ask_desc(cq:CallbackQuery, callback_data:CatalogCb, state:FSMContext):
    await cq.answer(); await state.set_state('submit_desc'); await state.update_data(target_type=callback_data.type)
    await cq.message.answer('<b>➕ Заявка</b>\n\nНапиши описание материала одним сообщением.')

@router.message(F.text)
async def got_desc(m:Message, state:FSMContext):
    if await state.get_state()!='submit_desc': return
    await state.update_data(description=m.text); await state.set_state('submit_file')
    await m.answer('Теперь отправь файл, фото, GIF или документ.')

@router.message(F.content_type.in_({'photo','document','animation','video'}))
async def got_file(m:Message, state:FSMContext, session, db_user):
    if await state.get_state()!='submit_file': return
    data=await state.get_data(); file_id=None; name=None; mime=None
    if m.photo: file_id=m.photo[-1].file_id; name='photo.jpg'; mime='image/jpeg'
    elif m.document: file_id=m.document.file_id; name=m.document.file_name; mime=m.document.mime_type
    elif m.animation: file_id=m.animation.file_id; name='animation.gif'; mime='image/gif'
    elif m.video: file_id=m.video.file_id; name='video.mp4'; mime='video/mp4'
    sub=Submission(user_id=db_user.id,target_type=data.get('target_type','file'),description=data.get('description',''),telegram_file_id=file_id,file_name=name,mime_type=mime)
    session.add(sub); await session.commit(); await session.refresh(sub); await state.clear()
    await m.answer('<b>✅ Заявка отправлена</b>\n<i>Ваш файл отправлен администратору на проверку.</i>', reply_markup=back_home())
    s=get_settings()
    if s.support_group_id:
        try:
            await m.bot.send_message(s.support_group_id, f'<b>📨 Новая заявка #{sub.id}</b>\n\n<b>Пользователь:</b> {m.from_user.full_name}\n<b>ID:</b> <code>{m.from_user.id}</code>\n<b>Username:</b> @{m.from_user.username or "нет"}\n<b>Раздел:</b> {sub.target_type}\n\n{sub.description}')
        except Exception: pass
