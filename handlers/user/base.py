from loader import dp
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.menu.kbds import base_menu


@dp.message_handler(Command('start'))
async def start(msg: Message):
    await msg.answer("""Greetings! This is just a test bot. The main purpose for it \
in the future is to create a complete helper bot for the beauty saloons. \
Use /help to see available commands.""",
                     reply_markup=base_menu)


@dp.message_handler(Command('help'))
async def show_help(msg: Message):
    await msg.answer("""/admin - use Admin Interface
/service - sign up for a Service""", reply_markup=ReplyKeyboardRemove())
