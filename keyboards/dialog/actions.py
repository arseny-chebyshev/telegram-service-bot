from loader import db_session
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy import select
from models.table_models import Service, Master


async def cancel(c: CallbackQuery, b: Button, d: DialogManager):
    await c.message.delete()
    await c.message.answer(text=f"Operation is canceled.")
    await d.mark_closed()
    await d.data['state'].reset_state(with_data=True)


async def get_services_all(**kwargs):
    async with db_session() as session:
        result = await session.execute(select(Service))
        await session.commit()
    service_list = [(service, service.service_id) for service in result.scalars()]
    return {"services": service_list}


async def get_masters_all(**kwargs):
    async with db_session() as session:
        result = await session.execute(select(Master))
        await session.commit()
    master_list = [(master, master.master_id) for master in result.scalars()]
    return {"masters": master_list}
