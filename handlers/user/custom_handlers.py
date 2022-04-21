from loader import dp
from aiogram.dispatcher.filters import Command
from aiogram.types import Message


@dp.message_handler(Command('foo'))
async def x(msg: Message):
    await msg.answer(text='bar')


@dp.message_handler(Command('Bar'))
async def x(msg: Message):
    await msg.answer(text='Foo')
