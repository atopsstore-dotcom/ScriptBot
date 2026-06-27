from aiogram import Router, F
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message
from bot.callbacks import DonateCb
from bot.database import Donation
router=Router()

@router.callback_query(DonateCb.filter(F.action=='pay'))
async def pay(cq:CallbackQuery, callback_data:DonateCb):
    await cq.answer()
    amount=max(callback_data.amount,1)
    await cq.message.answer_invoice(title='Поддержка ScriptBot', description='Донат на развитие проекта', payload=f'donate:{cq.from_user.id}:{amount}', currency='XTR', prices=[LabeledPrice(label='Stars', amount=amount)], provider_token='')

@router.pre_checkout_query()
async def pre(q:PreCheckoutQuery):
    await q.answer(ok=True)

@router.message(F.successful_payment)
async def success(m:Message, session, db_user):
    p=m.successful_payment
    d=Donation(user_id=db_user.id,amount=p.total_amount,currency=p.currency,invoice_payload=p.invoice_payload,telegram_payment_charge_id=p.telegram_payment_charge_id,provider_payment_charge_id=p.provider_payment_charge_id)
    session.add(d); await session.commit()
    await m.answer('<b>✅ Спасибо за поддержку!</b>\n<i>Ваш донат помогает развивать ScriptBot.</i>')
