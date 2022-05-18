from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


def is_service_selected(async_func):
    async def wrapper(c: CallbackQuery, b: Button, d: DialogManager):
        if 'r_service' in d.data['aiogd_context'].widget_data.keys():
            await async_func(c, b, d)
        else:
            await c.answer("Please select a service first")
    return wrapper


def is_master_selected(async_func):
    async def wrapper(c: CallbackQuery, b: Button, d: DialogManager):
        if 'r_master' in d.data['aiogd_context'].widget_data.keys():
            await async_func(c, b, d)
        else:
            await c.answer("Please select a master first")
    return wrapper


def is_schedule_selected(async_func):
    async def wrapper(c: CallbackQuery, b: Button, d: DialogManager):
        if 'r_hour' in d.data['aiogd_context'].widget_data.keys():
            await async_func(c, b, d)
        else:
            await c.answer("Please select an hour first")
    return wrapper
