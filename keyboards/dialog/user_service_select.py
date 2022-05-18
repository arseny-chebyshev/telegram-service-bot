import operator
from datetime import date
from loader import db_session
from filters.base import is_date_valid
from filters.user_dialog import is_service_selected, is_master_selected, is_schedule_selected
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Radio, Button, Group, Calendar
from aiogram_dialog.widgets.text import Format, Const
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import VARCHAR
from states.user import ServiceDialog, RegisterUser
from keyboards.menu.kbds import request_phone_button_kbd
from models.table_models import Service, Schedule, Master, service_master_table, schedule_master_table
from .admin_service_multiselect import get_services_all
from .actions import cancel


async def get_master_for_service(**kwargs) -> dict:
    service_id = kwargs['aiogd_context'].widget_data['r_service']
    datetime_id = kwargs['aiogd_context'].widget_data['r_hour']
    subquery = select(service_master_table.c.master).\
        where(service_master_table.c.service == int(service_id)).\
        filter(service_master_table.c.master.in_(select(schedule_master_table.c.master).
               where((schedule_master_table.c.time == int(datetime_id)) &
               schedule_master_table.c.is_free == True)))

    query = select(Master).filter(Master.master_id.in_(subquery))
    async with db_session() as session:
        result = await session.execute(query)
        await session.commit()
    master_list = [(master, master.master_id) for master in result.scalars()]
    return {"masters": master_list}


async def get_hour_for_date(**kwargs):
    calendar_date = kwargs['aiogd_context'].widget_data['calendar_date']
    async with db_session() as session:
        result = await session.execute(select(Schedule).
                                       where(Schedule.schedule_time.
                                       cast(VARCHAR).startswith(str(calendar_date))))
        await session.commit()
    hour_list = [(schedule, schedule.schedule_id) for schedule in result.scalars()]
    return {"hours": hour_list}


@is_service_selected
async def select_schedule_for_service(c: CallbackQuery, b: Button, d: DialogManager):
    await d.switch_to(ServiceDialog.select_schedule)


@is_date_valid
async def select_hour_for_schedule(c: CallbackQuery, widget, d: DialogManager, widget_date: date):
    d.data['aiogd_context'].widget_data['calendar_date'] = widget_date
    await d.switch_to(ServiceDialog.select_hour)


@is_schedule_selected
async def select_master_for_service(c: CallbackQuery, b: Button, d: DialogManager) -> None:
    await d.switch_to(ServiceDialog.select_master)


@is_master_selected
async def apply_order(c: CallbackQuery, b: Button, d: DialogManager) -> None:
    widget_data = d.data['aiogd_context'].widget_data
    async with db_session() as session:
        service = (await session.execute(select(Service).
                                         filter(Service.service_id == int
                                         (widget_data['r_service'])))).first()[0]
        schedule = (await session.execute(select(Schedule).
                                              filter(Schedule.schedule_id == int(widget_data['r_hour'])))).first()[0]
        master = (await session.execute(select(Master).
                                        filter(Master.master_id == int(widget_data['r_master'])))).first()[0]
    await d.data['state'].update_data({"service": service,
                                       "schedule": schedule,
                                       "master": master
                                       })
    await c.message.delete()
    time = str(schedule.schedule_time)
    await c.message.answer(text=
    f"{service.service_name} at {time[11:16]} {time[8:10]}.{time[5:7]} with {master.master_name} chosen.")
    await c.message.answer("Please push the button below so we have your contacts.",
                           reply_markup=request_phone_button_kbd)
    await d.mark_closed()
    await RegisterUser.send_contact.set()


service_radio_keyboard = Window(Const('Choose service:'),
                                Group(Radio(Format("✓ {item[0].service_name}"),
                                            Format("{item[0].service_name}"),
                                            id="r_service", items='services',
                                            item_id_getter=operator.itemgetter(1)),
                                      width=2),
                                Group(Button(Const("Search for schedule"),
                                             on_click=select_schedule_for_service,
                                             id='search_schedule'),
                                      Button(Const("Cancel"),
                                             on_click=cancel,
                                             id='cancel')),
                                getter=get_services_all,
                                state=ServiceDialog.select_service)

calendar_keyboard = Window(Const('Choose date:'),
                           Calendar(id='calendar_date',
                                    on_click=select_hour_for_schedule),
                           Button(Const("Cancel"), id='cancel', on_click=cancel),
                           state=ServiceDialog.select_schedule)

hour_keyboard = Window(Const('Select hour:'),
                       Group(Radio(Format("✓ {item[0].schedule_time.hour}:00"),
                                   Format("{item[0].schedule_time.hour}:00"),
                                   id="r_hour", items='hours',
                                   item_id_getter=operator.itemgetter(1)),
                             width=2),
                       Button(Const("Search for master"),
                              on_click=select_master_for_service,
                              id='search_schedule'),
                       Button(Const("Cancel"), id='cancel', on_click=cancel),
                       state=ServiceDialog.select_hour,
                       getter=get_hour_for_date)

master_radio_keyboard = Window(Const('Choose master:'),
                               Group(Radio(Format("✓ {item[0].master_name}"),
                                           Format("{item[0].master_name}"),
                                           id="r_master", items='masters',
                                           item_id_getter=operator.itemgetter(1)),
                                     width=2),
                               Button(Const("Apply for service"),
                                      id='apply',
                                      on_click=apply_order,
                                      ),
                               Button(Const("Cancel"), id='cancel', on_click=cancel),
                               getter=get_master_for_service,
                               state=ServiceDialog.select_master)

user_service_dialog = Dialog(service_radio_keyboard,
                             calendar_keyboard,
                             hour_keyboard,
                             master_radio_keyboard)
