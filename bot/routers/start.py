from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from bot.config import get_settings
from bot.repo import counts
from bot.keyboards import main_menu, back_home, splash_menu, donate_menu, submit_menu
from bot.callbacks import MainCb
from bot.texts import start_text, INFO
from bot.services import show_page

router=Router()

@router.message(CommandStart())
async def start(m:Message, session, **kw):
    c=await counts(session); s=get_settings()
    await show_page(m, start_text(s.bot_name,c,s.creator), main_menu())

@router.callback_query(MainCb.filter(F.action=='home'))
async def home(cq:CallbackQuery, session, **kw):
    c=await counts(session); s=get_settings(); await cq.answer()
    await show_page(cq, start_text(s.bot_name,c,s.creator), main_menu())

@router.callback_query(MainCb.filter(F.action=='info'))
async def info(cq:CallbackQuery):
    await cq.answer(); await show_page(cq, INFO, back_home())

@router.callback_query(MainCb.filter(F.action=='inline'))
async def inline(cq:CallbackQuery):
    await cq.answer()
    await show_page(cq, '<b>🔎 Поиск</b>\n\n<i>В этой версии поиск работает внутри каталога. Открой нужный раздел и выбери материал.</i>', back_home())

@router.callback_query(MainCb.filter(F.action=='splash'))
async def splash(cq:CallbackQuery):
    await cq.answer(); await show_page(cq, '<b>🎞 Заставки</b>\n\nСоздай boot-заставку или найди готовые материалы.', splash_menu())

@router.callback_query(MainCb.filter(F.action=='submit'))
async def submit(cq:CallbackQuery):
    await cq.answer(); await show_page(cq, '<b>➕ Добавить своё</b>\n\nВыбери раздел, куда хочешь отправить материал на проверку.', submit_menu())

@router.callback_query(MainCb.filter(F.action=='support'))
async def support(cq:CallbackQuery, state):
    await cq.answer(); await state.set_state('support_message')
    await show_page(cq, '<b>🆘 Поддержка</b>\n\n<i>Опиши проблему одним сообщением. Можно прикрепить фото или файл.</i>', back_home())

@router.callback_query(MainCb.filter(F.action=='donate'))
async def donate(cq:CallbackQuery):
    s=get_settings(); await cq.answer()
    await show_page(cq, '<b>⭐ Донаты</b>\n\n<i>Поддержи развитие ScriptBot через Telegram Stars.</i>', donate_menu([s.donation_preset_1,s.donation_preset_2,s.donation_preset_3,s.donation_preset_4]))

@router.message(Command('paysupport'))
async def paysupport(m:Message):
    await m.answer('<b>⭐ Поддержка платежей</b>\n\nНапиши в 🆘 Поддержку и укажи дату платежа, сумму и свой user_id.')
