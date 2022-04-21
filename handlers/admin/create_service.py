from loader import dp

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_dialog import DialogManager
from states.admin import AdminStates
from keyboards.dialog.admin_master_multiselect import MasterMultiselect


@dp.message_handler(Text(equals=['ADD SERVICE']), state=AdminStates.admin_state)
async def add_master_to_db(msg: Message):
    await msg.answer("Insert service name:", reply_markup=ReplyKeyboardRemove())
    await MasterMultiselect.inserting_price.set()


@dp.message_handler(state=MasterMultiselect.inserting_price)
async def add_price(msg: Message, state: FSMContext):
    await state.update_data({'service': msg.text})
    await msg.answer("Insert price for service:")
    await MasterMultiselect.inserting_service.set()


@dp.message_handler(state=MasterMultiselect.inserting_service)
async def choose_services_for_master(msg: Message, dialog_manager: DialogManager, state: FSMContext):
    await state.update_data({'price': msg.text})
    await msg.answer(f"Service {(await state.get_data())['service']} created.")
    await dialog_manager.start(MasterMultiselect.inserting_service)
