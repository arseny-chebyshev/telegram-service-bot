from loader import bot, dp, storage
from settings import admin_id

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from states.admin import AdminStates
from keyboards.menu.kbds import admin_menu


async def send_to_admin(dispatcher):
    await bot.send_message(chat_id=admin_id, text='Starting..')


async def shutdown(dispatcher):
    await bot.send_message(chat_id=admin_id, text="Shutting down..")
    await bot.close()
    await storage.close()


@dp.message_handler(Command('admin'), state=None)
async def start_admin_panel(msg: Message):
    if int(msg.from_user.id) == int(admin_id):
        await msg.answer(f"Greetings, master. Choose command:", reply_markup=admin_menu)
        await AdminStates.admin_state.set()
    else:
        await msg.answer("No admin rights to do that. Sorry!")


@dp.message_handler(Text(equals='CANCEL'), state=AdminStates.admin_state)
async def cancel_admin_panel(msg: Message, state: FSMContext):
    await msg.answer("Admin mode canceled. Data is erased.", reply_markup=ReplyKeyboardRemove())
    await state.reset_state(with_data=True)
