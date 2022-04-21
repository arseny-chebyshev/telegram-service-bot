from loader import dp

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_dialog import DialogManager
from states.admin import AdminStates
from keyboards.dialog.admin_service_multiselect import ServiceMultiselect


@dp.message_handler(Text(equals=['ADD MASTER']), state=AdminStates.admin_state)
async def add_master_to_db(msg: Message):
    await msg.answer("Insert master name:", reply_markup=ReplyKeyboardRemove())
    await ServiceMultiselect.inserting_master.set()


@dp.message_handler(state=ServiceMultiselect.inserting_master)
async def choose_services_for_master(msg: Message, dialog_manager: DialogManager, state: FSMContext):
    await state.update_data({'master': msg.text})
    await msg.answer(f"Master {(await state.get_data())['master']} created.")
    await dialog_manager.start(ServiceMultiselect.inserting_master)
