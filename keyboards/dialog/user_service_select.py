import datetime
import operator
from datetime import date
from loader import db_session
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Radio, Button, Group, Calendar
from aiogram_dialog.widgets.text import Format, Const
from sqlalchemy import select, insert, text
from sqlalchemy.dialects.postgresql import VARCHAR
from models.table_models import Service, Master, Schedule, service_master_table, schedule_master_table
from .admin_service_multiselect import get_services_all
from .actions import cancel


class ServiceDialog(StatesGroup):
    select_service = State()
    select_master = State()
    select_schedule = State()
    select_hour = State()


async def get_master_for_service(**kwargs) -> dict:
    if 'r_hours' in kwargs['aiogd_context'].widget_data.keys():
        datetime_id = kwargs['aiogd_context'].widget_data['r_hours']
        subquery = select(schedule_master_table.c.master).\
            where((schedule_master_table.c.time == int(datetime_id)) &
                  (service_master_table.c.service == int(kwargs['aiogd_context'].widget_data['r_service'])))
    else:
        subquery = select(service_master_table.c.master).\
            where(service_master_table.c.service == int(kwargs['aiogd_context'].widget_data['r_service']))
    query = select(Master).filter(Master.master_id.in_(subquery))
    async with db_session() as session:
        result = await session.execute(query)
        await session.commit()
    master_list = [(master, master.master_id) for master in result.scalars()]
    return {"masters": master_list}


async def get_schedule_for_master(**kwargs) -> dict:
    pass


async def get_hour_for_date(**kwargs):
    schedule_date = kwargs['aiogd_context'].widget_data['schedule_date']
    async with db_session() as session:
        result = await session.execute(select(Schedule).
                                       where(Schedule.schedule_time.
                                       cast(VARCHAR).startswith(str(schedule_date))))
        await session.commit()
    hour_list = [(schedule, schedule.schedule_id) for schedule in result.scalars()]
    return {"hours": hour_list}


async def select_master_for_service(c: CallbackQuery, b: Button, d: DialogManager) -> None:
    await d.switch_to(ServiceDialog.select_master)


async def select_schedule_for_service(c: CallbackQuery, b: Button, d: DialogManager):
    await d.switch_to(ServiceDialog.select_schedule)


async def select_hour_for_schedule(c: CallbackQuery, widget, d: DialogManager, widget_date: date):
    if widget_date < datetime.date.today():
        await c.answer("Please select a future date")
    else:
        d.data['aiogd_context'].widget_data['schedule_date'] = widget_date
        await d.switch_to(ServiceDialog.select_hour)


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
                               Button(Const("Search for schedule"),
                                      id='search_schedule',
                                      on_click=select_schedule_for_service),
                               Button(Const("Cancel"), id='cancel', on_click=cancel),
                               getter=get_master_for_service,
                               state=ServiceDialog.select_master)

calendar_keyboard = Window(Const('Choose date:'),
                           Calendar(id='schedule_date',
                                    on_click=select_hour_for_schedule),
                           Button(Const("Cancel"), id='cancel', on_click=cancel),
                           state=ServiceDialog.select_schedule)

hour_keyboard = Window(Const('Select hour:'),
                       Group(Radio(Format("✓ {item[0].schedule_time.hour}:00"),
                                   Format("{item[0].schedule_time.hour}:00"),
                                   id="r_hours", items='hours',
                                   item_id_getter=operator.itemgetter(1)),
                             width=2),
                       Button(Const("Search for master"),
                              on_click=select_master_for_service,
                              id='search_schedule'),
                       state=ServiceDialog.select_hour,
                       getter=get_hour_for_date)

user_service_dialog = Dialog(service_radio_keyboard, master_radio_keyboard,
                             calendar_keyboard, hour_keyboard)
