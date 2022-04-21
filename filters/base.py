from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message


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
