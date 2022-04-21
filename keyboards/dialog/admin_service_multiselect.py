import operator
from loader import db_session
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Multiselect, Button, Group
from aiogram_dialog.widgets.text import Format, Const
from sqlalchemy import select, insert
from models.table_models import Service, Master, service_master_table
from .actions import cancel


class ServiceMultiselect(StatesGroup):
    inserting_master = State()


async def get_services_all(**kwargs):
    async with db_session() as session:
        result = await session.execute(select(Service))
        services = [res for res in result.scalars()]
        await session.commit()
    service_list = [(service, service.service_id) for service in services]
    return {"services": service_list}


async def add_services_to_master(c: CallbackQuery, b: Button, d: DialogManager):
    services = d.data['aiogd_context'].widget_data['m_services']
    await d.data['state'].update_data({'services': services})
    dialog_data = await d.data['state'].get_data()
    master = Master(master_name=f"{dialog_data['master']}")
    async with db_session() as session:
        session.add(master)
        await session.flush()
        for _ in dialog_data['services']:
            await session.execute(service_master_table.insert().
                                  values(service=int(_), master=master.master_id))
        await session.commit()
    await c.message.delete()
    await c.message.answer(text=f"Services added to master. Thank you!")
    await d.mark_closed()
    await d.data['state'].reset_state(with_data=True)


add_service_dialog = Dialog(Window(Const('Choose services:'),
                                   Group(Multiselect(
                                             Format("✓ {item[0].service_name}"),
                                             Format("{item[0].service_name}"),
                                             id="m_services", items='services',
                                             item_id_getter=operator.itemgetter(1)),
                                         width=2),
                                   Group(Button(Const("Submit"),
                                                id='submit',
                                                on_click=add_services_to_master),
                                         Button(Const("Cancel"),
                                                id='cancel',
                                                on_click=cancel)),
                            getter=get_services_all,
                            state=ServiceMultiselect.inserting_master))
