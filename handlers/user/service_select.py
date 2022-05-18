import aiogram.types
from sqlalchemy import select, update
from loader import dp, db_session
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram.dispatcher import FSMContext
from models.table_models import Client, Order, schedule_master_table
from states.user import RegisterUser
from keyboards.dialog.user_service_select import ServiceDialog


@dp.message_handler(commands=["service"], state=None)
async def select_service(msg: Message, dialog_manager: DialogManager):
    await ServiceDialog.select_service.set()
    await dialog_manager.start(ServiceDialog.select_service)


@dp.message_handler(state=RegisterUser.send_contact, content_types=aiogram.types.ContentType.CONTACT)
async def process_contact(msg: Message, state: FSMContext):
    data = await state.get_data()
    client_id, client_phone, client_name = msg.contact['user_id'], msg.contact['phone_number'], \
        f"{msg.contact['last_name']} {msg.contact['first_name']}"
    service, schedule, master = data['service'], data['schedule'], data['master']
    async with db_session() as session:
        client = (await session.execute(select(Client).filter(Client.client_id == client_id))).first()
        if not client:
            client = Client(client_id=client_id, client_name=client_name,
                            client_tel=client_phone, is_regular=False)
            session.add(client)
            await session.flush()
        else:
            client = client[0]
            client.is_regular = True
            session.add(client)
            await session.flush()
        order = Order(order_service=service.service_id, order_client=client.client_id,
                      order_master=master.master_id, order_time=schedule.schedule_id)
        session.add(order)
        await session.execute(update(schedule_master_table).
                              where((schedule_master_table.c.time == schedule.schedule_id) &
                              (schedule_master_table.c.master == master.master_id)).
                              values(is_free=False))
        await session.flush()
        await session.commit()
    await msg.answer("Thank you for sharing!")
    await msg.answer(f"Order #{order.order_id} has been created.")
    await state.reset_state(with_data=True)
