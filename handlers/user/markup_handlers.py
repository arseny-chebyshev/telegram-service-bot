from loader import dp

from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.menu.menu_keyboard import func_menu


@dp.message_handler(Command('menu'))
async def show_menu(msg: Message):
    await msg.answer("Here is the menu", reply_markup=func_menu)


@dp.message_handler(Text(equals=['First Function', 'Second Function', 'Third Function']))
async def do_menu_function(msg: Message):
    await msg.answer(f'Function {msg.text} has been chosen', reply_markup=ReplyKeyboardRemove())
