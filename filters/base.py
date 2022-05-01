import datetime

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, msg: Message):
        from settings import admin_id
        if int(msg.from_user.id) == int(admin_id):
            return True
        else:
            await msg.answer("No admin rights to do that. Sorry!")
            return False


def is_date_valid(async_func):
    async def wrapper(c: CallbackQuery, widget, d: DialogManager, widget_date: datetime.date):
        if widget_date >= datetime.date.today():
            await async_func(c, widget, d, widget_date)
        else:
            await c.answer("Please select a future date")
    return wrapper
