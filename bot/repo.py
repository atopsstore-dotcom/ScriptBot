from datetime import datetime
from sqlalchemy import select, func
from bot.database import User, ContentItem, Submission, Donation, SupportTicket, Setting, Device, Category, AdminActionLog

async def upsert_user(s, tg_user, admin_ids):
    res=await s.execute(select(User).where(User.telegram_id==tg_user.id))
    u=res.scalar_one_or_none()
    if u:
        u.username=tg_user.username; u.first_name=tg_user.first_name; u.last_name=tg_user.last_name; u.language_code=tg_user.language_code; u.is_admin=tg_user.id in admin_ids; u.last_active_at=datetime.utcnow()
    else:
        u=User(telegram_id=tg_user.id, username=tg_user.username, first_name=tg_user.first_name, last_name=tg_user.last_name, language_code=tg_user.language_code, is_admin=tg_user.id in admin_ids)
        s.add(u)
    await s.commit(); await s.refresh(u); return u

async def counts(s):
    return {
        'users': await s.scalar(select(func.count(User.id))) or 0,
        'files': await s.scalar(select(func.count(ContentItem.id)).where(ContentItem.type=='file')) or 0,
        'schemes': await s.scalar(select(func.count(ContentItem.id)).where(ContentItem.type=='scheme')) or 0,
        'splash': await s.scalar(select(func.count(ContentItem.id)).where(ContentItem.type=='splash')) or 0,
        'pending': await s.scalar(select(func.count(Submission.id)).where(Submission.status=='pending')) or 0,
        'stars': await s.scalar(select(func.coalesce(func.sum(Donation.amount),0))) or 0,
        'tickets': await s.scalar(select(func.count(SupportTicket.id)).where(SupportTicket.status=='open')) or 0,
    }
async def get_setting(s,key,default=''):
    x=(await s.execute(select(Setting).where(Setting.key==key))).scalar_one_or_none()
    return x.value if x else default
async def set_setting(s,key,value):
    x=(await s.execute(select(Setting).where(Setting.key==key))).scalar_one_or_none()
    if x: x.value=value
    else: s.add(Setting(key=key,value=value))
    await s.commit()
async def log(s, admin_id, action, payload=''):
    s.add(AdminActionLog(admin_user_id=admin_id, action=action, payload=payload)); await s.commit()
