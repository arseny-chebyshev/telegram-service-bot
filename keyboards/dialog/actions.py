from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def cancel(c: CallbackQuery, b: Button, d: DialogManager):
    await c.message.delete()
    await c.message.answer(text=f"Operation is canceled.")
    await d.mark_closed()
    await d.data['state'].reset_state(with_data=True)
