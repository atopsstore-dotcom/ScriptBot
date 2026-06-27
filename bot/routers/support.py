from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from bot.config import get_settings
from bot.database import SupportTicket
from bot.callbacks import TicketCb
from bot.keyboards import ticket_admin
router=Router()

@router.message(F.text == '/connect_support_group')
async def connect_group(m:Message):
    s=get_settings()
    if m.from_user.id not in s.admin_ids: return
    await m.answer(f'✅ ID этой группы: <code>{m.chat.id}</code>\nУкажи его в <code>SUPPORT_GROUP_ID</code> и перезапусти контейнер.')

@router.message(F.text)
async def support_msg(m:Message, state:FSMContext, session, db_user):
    if await state.get_state()!='support_message': return
    s=get_settings(); await state.clear()
    ticket=SupportTicket(user_id=db_user.id, group_id=s.support_group_id)
    session.add(ticket); await session.commit(); await session.refresh(ticket)
    await m.answer('<b>✅ Запрос отправлен</b>\n<i>Ваш запрос на рассмотрении.</i>')
    if s.support_group_id:
        try:
            thread_id=None
            try:
                topic=await m.bot.create_forum_topic(s.support_group_id, name=f'🆘 {m.from_user.username or m.from_user.id} | {m.from_user.first_name or "user"}')
                thread_id=topic.message_thread_id; ticket.thread_id=thread_id; await session.commit()
            except Exception: pass
            await m.bot.send_message(s.support_group_id, f'<b>🆘 Тикет #{ticket.id}</b>\n\n<b>Имя:</b> {m.from_user.full_name}\n<b>ID:</b> <code>{m.from_user.id}</code>\n<b>Username:</b> @{m.from_user.username or "нет"}\n\n<b>Сообщение:</b>\n{m.text}', message_thread_id=thread_id, reply_markup=ticket_admin(ticket.id))
        except Exception: pass

@router.callback_query(TicketCb.filter(F.action=='claim'))
async def claim(cq:CallbackQuery, callback_data:TicketCb, session):
    s=get_settings()
    if cq.from_user.id not in s.admin_ids: return await cq.answer('Нет доступа', show_alert=True)
    t=(await session.execute(select(SupportTicket).where(SupportTicket.id==callback_data.id))).scalar_one_or_none()
    if not t: return await cq.answer('Тикет не найден', show_alert=True)
    if t.assigned_admin_id and t.assigned_admin_id != cq.from_user.id:
        return await cq.answer(f'Этому пользователю уже помогает ID {t.assigned_admin_id}', show_alert=True)
    t.assigned_admin_id=cq.from_user.id; await session.commit()
    await cq.answer('Тикет закреплён за вами')
    await cq.message.answer(f'✅ Тикет #{t.id} закреплён за <code>{cq.from_user.id}</code>')

@router.callback_query(TicketCb.filter(F.action=='close'))
async def close(cq:CallbackQuery, callback_data:TicketCb, session):
    t=(await session.execute(select(SupportTicket).where(SupportTicket.id==callback_data.id))).scalar_one_or_none()
    if not t: return await cq.answer('Не найден', show_alert=True)
    if t.assigned_admin_id and t.assigned_admin_id != cq.from_user.id: return await cq.answer('Тикет закреплён за другим сотрудником', show_alert=True)
    t.status='closed'; t.closed_at=datetime.utcnow(); await session.commit(); await cq.answer('Закрыто')
    await cq.message.answer(f'❌ Тикет #{t.id} закрыт')
