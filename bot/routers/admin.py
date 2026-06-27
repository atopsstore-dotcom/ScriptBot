from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from bot.config import get_settings
from bot.keyboards import admin_menu
from bot.callbacks import AdminCb
from bot.repo import counts
from bot.backup import create_backup
from bot.services import show_page
router=Router()

def is_admin(uid:int): return uid in get_settings().admin_ids

@router.message(Command('admin'))
async def admin(m:Message, session):
    if not is_admin(m.from_user.id): return await m.answer('⛔ У вас нет доступа')
    c=await counts(session)
    text=(f'<b>⚙️ Админ-панель ScriptBot</b>\n\n'
          f'• <b>Пользователей:</b> {c["users"]}\n'
          f'• <b>Файлов:</b> {c["files"]}\n'
          f'• <b>Схем:</b> {c["schemes"]}\n'
          f'• <b>Заставок:</b> {c["splash"]}\n'
          f'• <b>Заявок:</b> {c["pending"]}\n'
          f'• <b>Тикетов:</b> {c["tickets"]}')
    await show_page(m, text, admin_menu())

@router.callback_query(AdminCb.filter())
async def admin_cb(cq:CallbackQuery, callback_data:AdminCb, session):
    if not is_admin(cq.from_user.id): return await cq.answer('Нет доступа', show_alert=True)
    await cq.answer(); sec=callback_data.section
    if sec=='stats':
        c=await counts(session); text='\n'.join([f'• <b>{k}:</b> {v}' for k,v in c.items()])
        return await show_page(cq, '<b>📊 Статистика</b>\n\n'+text, admin_menu())
    if sec=='settings':
        return await show_page(cq, '<b>⚙️ Настройки</b>\n\nТокен, группа поддержки, название и обложка настраиваются через <code>.env</code>. После изменения выполните <code>docker compose restart</code>.', admin_menu())
    if sec=='cover':
        return await show_page(cq, '<b>🖼 Обложка</b>\n\nФайл по умолчанию: <code>assets/default.png</code>\nМожно заменить файл и перезапустить контейнер.', admin_menu())
    if sec=='subs':
        return await show_page(cq, '<b>📨 Заявки</b>\n\nЗаявки от пользователей приходят сюда и в группу поддержки, если указан <code>SUPPORT_GROUP_ID</code>.', admin_menu())
    return await show_page(cq, f'<b>{callback_data.section}</b>\n\nРаздел доступен. Управление будет расширяться в следующих версиях ScriptBot.', admin_menu())

@router.message(Command('backup'))
async def backup(m:Message):
    if not is_admin(m.from_user.id): return
    path=create_backup(); await m.answer_document(FSInputFile(path), caption='<b>✅ Бэкап создан</b>')
