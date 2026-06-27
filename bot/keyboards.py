from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.callbacks import MainCb, AdminCb, CatalogCb, TicketCb, DonateCb

def main_menu():
    kb=InlineKeyboardBuilder()
    kb.button(text='🔎 Поиск', callback_data=MainCb(action='inline').pack())
    kb.button(text='📁 Файлы', callback_data=CatalogCb(type='file', action='list').pack())
    kb.button(text='🧩 Схемы', callback_data=CatalogCb(type='scheme', action='list').pack())
    kb.button(text='🎞 Заставки', callback_data=MainCb(action='splash').pack())
    kb.button(text='➕ Добавить своё', callback_data=MainCb(action='submit').pack())
    kb.button(text='🆘 Поддержка', callback_data=MainCb(action='support').pack())
    kb.button(text='ℹ️ Информация', callback_data=MainCb(action='info').pack())
    kb.button(text='⭐ Донаты', callback_data=MainCb(action='donate').pack())
    kb.adjust(2,2,2,2)
    return kb.as_markup()

def back_home():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🏠 Меню', callback_data=MainCb(action='home').pack())]])

def admin_menu():
    kb=InlineKeyboardBuilder()
    for text, sec in [('📁 Файлы','files'),('🧩 Схемы','schemes'),('🎞 Заставки','splash'),('📱 Устройства','devices'),('👥 Пользователи','users'),('📨 Заявки','subs'),('📢 Рассылки','broadcast'),('📣 Реклама','ads'),('⭐ Донаты','donations'),('📊 Статистика','stats'),('🆘 Поддержка','support'),('🖼 Обложка','cover'),('⚙️ Настройки','settings')]:
        kb.button(text=text, callback_data=AdminCb(section=sec).pack())
    kb.button(text='🏠 В меню', callback_data=MainCb(action='home').pack())
    kb.adjust(2)
    return kb.as_markup()

def splash_menu():
    kb=InlineKeyboardBuilder()
    kb.button(text='🎨 Создать свою', callback_data=CatalogCb(type='splash', action='create').pack())
    kb.button(text='🔎 Найти готовые', callback_data=CatalogCb(type='splash', action='list').pack())
    kb.button(text='🏠 Меню', callback_data=MainCb(action='home').pack())
    kb.adjust(1)
    return kb.as_markup()

def splash_create_menu():
    kb=InlineKeyboardBuilder()
    kb.button(text='🖼 Фото-заставка', callback_data=CatalogCb(type='splash', action='photo').pack())
    kb.button(text='🎞 GIF-заставка', callback_data=CatalogCb(type='splash', action='gif').pack())
    kb.button(text='🎬 Видео → GIF', callback_data=CatalogCb(type='splash', action='video').pack())
    kb.button(text='🏠 Меню', callback_data=MainCb(action='home').pack())
    kb.adjust(1)
    return kb.as_markup()

def submit_menu():
    kb=InlineKeyboardBuilder()
    kb.button(text='📁 В файлы', callback_data=CatalogCb(type='file', action='submit').pack())
    kb.button(text='🧩 В схемы', callback_data=CatalogCb(type='scheme', action='submit').pack())
    kb.button(text='🎞 В заставки', callback_data=CatalogCb(type='splash', action='submit').pack())
    kb.button(text='🏠 Меню', callback_data=MainCb(action='home').pack())
    kb.adjust(1)
    return kb.as_markup()

def donate_menu(presets):
    kb=InlineKeyboardBuilder()
    for amount in presets: kb.button(text=f'⭐ {amount}', callback_data=DonateCb(action='pay', amount=amount).pack())
    kb.button(text='✍️ Ввести свою сумму', callback_data=DonateCb(action='custom').pack())
    kb.button(text='🏠 Меню', callback_data=MainCb(action='home').pack())
    kb.adjust(2,2,1,1)
    return kb.as_markup()

def ticket_admin(ticket_id:int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✅ Помочь', callback_data=TicketCb(action='claim', id=ticket_id).pack())],
        [InlineKeyboardButton(text='🚫 Заблокировать', callback_data=TicketCb(action='block', id=ticket_id).pack()), InlineKeyboardButton(text='❌ Закрыть', callback_data=TicketCb(action='close', id=ticket_id).pack())]
    ])

def pager(type_, page, has_prev, has_next):
    row=[]
    if has_prev: row.append(InlineKeyboardButton(text='⬅️', callback_data=CatalogCb(type=type_, action='list', page=page-1).pack()))
    if has_next: row.append(InlineKeyboardButton(text='➡️', callback_data=CatalogCb(type=type_, action='list', page=page+1).pack()))
    return InlineKeyboardMarkup(inline_keyboard=[row, [InlineKeyboardButton(text='🏠 Меню', callback_data=MainCb(action='home').pack())]] if row else [[InlineKeyboardButton(text='🏠 Меню', callback_data=MainCb(action='home').pack())]])
