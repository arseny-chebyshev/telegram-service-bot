import operator
from loader import db_session
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Multiselect, Button, Group
from aiogram_dialog.widgets.text import Format, Const
from models.table_models import Master, service_master_table
from states.admin import ServiceMultiselect
from .actions import cancel, get_services_all


async def add_services_to_master(c: CallbackQuery, b: Button, d: DialogManager):
    services = d.data['aiogd_context'].widget_data['m_services']
    await d.data['state'].update_data({'services': services})
    dialog_data = await d.data['state'].get_data()
    master = Master(master_name=f"{dialog_data['master']}")
    async with db_session() as session:
        session.add(master)
        await session.flush()  # flush to create master object with id and other entities
        service_master_objects = [{'service': int(_), 'master': master.master_id}
                                  for _ in dialog_data['services']]
        await session.execute(service_master_table.insert().
                              values(service_master_objects))
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
