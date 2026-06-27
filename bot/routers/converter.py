from pathlib import Path
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext
from bot.callbacks import CatalogCb
from bot.config import get_settings
from bot.converter import convert_photo, convert_gif, convert_video, ConvertError
from bot.keyboards import back_home
router=Router()

@router.callback_query(CatalogCb.filter((F.type=='splash') & (F.action.in_({'photo','gif','video'}))))
async def ask_file(cq:CallbackQuery, callback_data:CatalogCb, state:FSMContext):
    await cq.answer(); await state.set_state('convert_wait_file'); await state.update_data(kind=callback_data.action)
    names={'photo':'фото','gif':'GIF','video':'видео'}
    await cq.message.answer(f'<b>🎞 Конвертер</b>\n\nОтправь {names[callback_data.action]} для конвертации в формат Bruce/M5Stick <code>240×135</code>.')

@router.message(F.text == '/cancel')
async def cancel(m:Message, state:FSMContext):
    await state.clear(); await m.answer('❌ Отменено', reply_markup=back_home())

@router.message(F.content_type.in_({'photo','document','animation','video'}))
async def convert_any(m:Message, bot:Bot, state:FSMContext):
    data=await state.get_data()
    if await state.get_state() != 'convert_wait_file': return
    s=get_settings(); temp=Path(s.temp_path); temp.mkdir(parents=True, exist_ok=True)
    try:
        kind=data.get('kind','photo')
        if m.photo: file_id=m.photo[-1].file_id; ext='.jpg'
        elif m.animation: file_id=m.animation.file_id; ext='.gif'
        elif m.video: file_id=m.video.file_id; ext='.mp4'
        elif m.document: file_id=m.document.file_id; ext=Path(m.document.file_name or 'file.bin').suffix or '.bin'
        else: return await m.answer('Отправь фото, GIF или видео.')
        f=await bot.get_file(file_id); src=temp/f'{m.from_user.id}_{m.message_id}{ext}'
        await bot.download_file(f.file_path, src)
        await m.answer('⏳ Конвертирую файл...')
        if kind=='photo': out=await convert_photo(src,s.converted_path,s.splash_width,s.splash_height)
        elif kind=='gif': out=await convert_gif(src,s.converted_path,s.splash_width,s.splash_height,s.splash_gif_fps,s.splash_gif_max_seconds)
        else: out=await convert_video(src,s.converted_path,s.splash_width,s.splash_height,s.splash_gif_fps,s.splash_gif_max_seconds)
        await state.clear()
        await m.answer_document(FSInputFile(out, filename='boot.gif' if out.endswith('.gif') else Path(out).name), caption='<b>✅ Готово</b>\n\nФайл подготовлен под Bruce/M5StickC PLUS2.')
    except ConvertError as e:
        await m.answer(f'<b>❌ Ошибка конвертации</b>\n<code>{str(e)[:900]}</code>', reply_markup=back_home())
    except Exception as e:
        await m.answer(f'<b>❌ Ошибка</b>\n<code>{str(e)[:900]}</code>', reply_markup=back_home())
