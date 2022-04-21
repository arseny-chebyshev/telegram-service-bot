import operator
from loader import db_session
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Radio, Button, Group
from aiogram_dialog.widgets.text import Format, Const
from sqlalchemy import select, insert
from models.table_models import Service, Master, service_master_table
from .admin_service_multiselect import get_services_all
from .actions import cancel


class ServiceDialog(StatesGroup):
    select_service = State()
    select_master = State()
    select_schedule = State()


async def get_master_for_service(**kwargs):
    async with db_session() as session:
        subquery = select(service_master_table.c.master).where(service_master_table.c.service == int
        (kwargs['aiogd_context'].widget_data['r_service']))

        query = select(Master).filter(Master.master_id.in_(subquery))
        result = await session.execute(query)
        masters = [res for res in result.scalars()]
        await session.commit()
    master_list = [(master, master.master_id) for master in masters]
    return {"masters": master_list}


async def get_schedule_for_service(**kwargs):
    pass


async def select_master_for_service(c: CallbackQuery, b: Button, d: DialogManager):
    await d.switch_to(ServiceDialog.select_master)


async def select_schedule_for_service(c: CallbackQuery, b: Button, d: DialogManager):
    pass


service_radio_keyboard = Window(Const('Choose service:'),
                                Group(Radio(Format("✓ {item[0].service_name}"),
                                            Format("{item[0].service_name}"),
                                            id="r_service", items='services',
                                            item_id_getter=operator.itemgetter(1)),
                                      width=2),
                                Group(Button(Const("Search for master"),
                                      on_click=select_master_for_service,
                                      id='search_master'),
                                      Button(Const("Search for schedule"),
                                      on_click=select_schedule_for_service,
                                      id='search_schedule')),
                                Button(Const("Cancel"), id='cancel', on_click=cancel),
                                getter=get_services_all,
                                state=ServiceDialog.select_service)

master_radio_keyboard = Window(Const('Choose master:'),
                               Group(Radio(Format("✓ {item[0].master_name}"),
                                           Format("{item[0].master_name}"),
                                           id="r_masters", items='masters',
                                           item_id_getter=operator.itemgetter(1)),
                                     width=2),
                               Button(Const("Cancel"), id='cancel', on_click=cancel),
                               getter=get_master_for_service,
                               state=ServiceDialog.select_master)

user_service_dialog = Dialog(service_radio_keyboard, master_radio_keyboard)
