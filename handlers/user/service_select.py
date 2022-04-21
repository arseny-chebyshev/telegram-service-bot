from loader import dp
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_dialog import DialogManager
from aiogram.dispatcher import FSMContext
from states.fsm_test import FsmTest
from keyboards.dialog.user_service_select import ServiceDialog


@dp.message_handler(commands=["service"], state=None)
async def select_service(msg: Message, dialog_manager: DialogManager):
    await ServiceDialog.select_service.set()
    await dialog_manager.start(ServiceDialog.select_service)
