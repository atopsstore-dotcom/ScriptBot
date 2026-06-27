from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select
from bot.callbacks import CatalogCb
from bot.database import ContentItem
from bot.keyboards import pager, splash_create_menu
from bot.services import show_page
router=Router()

@router.callback_query(CatalogCb.filter(F.action=='list'))
async def list_items(cq:CallbackQuery, callback_data:CatalogCb, session):
    await cq.answer(); page=max(callback_data.page,0); limit=6
    typ=callback_data.type
    q=await session.execute(select(ContentItem).where(ContentItem.type==typ, ContentItem.is_visible==True).order_by(ContentItem.created_at.desc()).offset(page*limit).limit(limit+1))
    items=q.scalars().all(); has_next=len(items)>limit; items=items[:limit]
    title={'file':'📁 Файлы','scheme':'🧩 Схемы','splash':'🎞 Заставки'}.get(typ,'Каталог')
    if not items:
        text=f'<b>{title}</b>\n\n<i>Пока пусто. Материалы появятся после добавления админом или одобрения заявок.</i>'
    else:
        lines=[f'<b>{title}</b>\n']
        for i,it in enumerate(items,1):
            lines.append(f'{i}. <b>{it.title}</b>\n<i>{it.description or "Без описания"}</i>')
        text='\n'.join(lines)
    await show_page(cq,text,pager(typ,page,page>0,has_next))

@router.callback_query(CatalogCb.filter((F.type=='splash') & (F.action=='create')))
async def splash_create(cq:CallbackQuery):
    await cq.answer(); await show_page(cq,'<b>🎨 Создать заставку</b>\n\nВыбери тип исходного файла.',splash_create_menu())
