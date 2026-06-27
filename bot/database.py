from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, BigInteger, select, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from bot.config import get_settings

class Base(DeclarativeBase): pass

def now(): return datetime.utcnow()

class User(Base):
    __tablename__='users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str|None] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str|None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str|None] = mapped_column(String(255), nullable=True)
    language_code: Mapped[str|None] = mapped_column(String(32), nullable=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    last_active_at: Mapped[datetime] = mapped_column(DateTime, default=now)

class Device(Base):
    __tablename__='devices'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(Text, default='')
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)

class Category(Base):
    __tablename__='categories'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_id: Mapped[int|None] = mapped_column(ForeignKey('categories.id'), nullable=True)
    device_id: Mapped[int|None] = mapped_column(ForeignKey('devices.id'), nullable=True)
    type: Mapped[str] = mapped_column(String(32), index=True) # files/schemes/splash
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, default='')
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)

class ContentItem(Base):
    __tablename__='content_items'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(32), index=True) # file/scheme/splash
    device_id: Mapped[int|None] = mapped_column(ForeignKey('devices.id'), nullable=True)
    category_id: Mapped[int|None] = mapped_column(ForeignKey('categories.id'), nullable=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, default='')
    telegram_file_id: Mapped[str|None] = mapped_column(Text, nullable=True)
    local_path: Mapped[str|None] = mapped_column(Text, nullable=True)
    file_name: Mapped[str|None] = mapped_column(String(255), nullable=True)
    mime_type: Mapped[str|None] = mapped_column(String(255), nullable=True)
    file_size: Mapped[int] = mapped_column(Integer, default=0)
    author_user_id: Mapped[int|None] = mapped_column(ForeignKey('users.id'), nullable=True)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=now)

class Submission(Base):
    __tablename__='submissions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    target_type: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(Text, default='')
    telegram_file_id: Mapped[str|None] = mapped_column(Text, nullable=True)
    local_path: Mapped[str|None] = mapped_column(Text, nullable=True)
    file_name: Mapped[str|None] = mapped_column(String(255), nullable=True)
    mime_type: Mapped[str|None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default='pending')
    admin_comment: Mapped[str] = mapped_column(Text, default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=now)

class Donation(Base):
    __tablename__='donations'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    amount: Mapped[int] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(String(16), default='XTR')
    invoice_payload: Mapped[str] = mapped_column(String(255))
    telegram_payment_charge_id: Mapped[str|None] = mapped_column(String(255), nullable=True)
    provider_payment_charge_id: Mapped[str|None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)

class SupportTicket(Base):
    __tablename__='support_tickets'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    status: Mapped[str] = mapped_column(String(32), default='open')
    group_id: Mapped[int|None] = mapped_column(BigInteger, nullable=True)
    thread_id: Mapped[int|None] = mapped_column(BigInteger, nullable=True)
    assigned_admin_id: Mapped[int|None] = mapped_column(BigInteger, nullable=True)
    first_message_id: Mapped[int|None] = mapped_column(BigInteger, nullable=True)
    last_message_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    closed_at: Mapped[datetime|None] = mapped_column(DateTime, nullable=True)

class Setting(Base):
    __tablename__='settings'
    key: Mapped[str] = mapped_column(String(128), primary_key=True)
    value: Mapped[str] = mapped_column(Text, default='')

class AdminActionLog(Base):
    __tablename__='admin_actions_log'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    admin_user_id: Mapped[int] = mapped_column(BigInteger)
    action: Mapped[str] = mapped_column(String(255))
    payload: Mapped[str] = mapped_column(Text, default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)

settings=get_settings()
engine=create_async_engine(settings.database_url, future=True)
SessionLocal=async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with SessionLocal() as s:
        q=await s.execute(select(Device).where(Device.is_default==True))
        if not q.scalar_one_or_none():
            s.add(Device(title=settings.default_device_name, slug='default', is_default=True))
            await s.commit()
