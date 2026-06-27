from aiogram.filters.callback_data import CallbackData

class MainCb(CallbackData, prefix='m'):
    action: str
class AdminCb(CallbackData, prefix='a'):
    section: str
    action: str='open'
    id: int=0
class CatalogCb(CallbackData, prefix='c'):
    type: str
    action: str
    id: int=0
    page: int=0
class TicketCb(CallbackData, prefix='t'):
    action: str
    id: int=0
class DonateCb(CallbackData, prefix='d'):
    action: str
    amount: int=0
