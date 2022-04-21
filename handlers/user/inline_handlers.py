from loader import dp

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline.callback_datas import purchase_callback
from keyboards.inline.choice_buttons import inline_keyboard, apple_keyboard, peach_keyboard


@dp.message_handler(Command('items'))
async def show_items(msg: Message):
    await msg.answer(text='Here are our items', reply_markup=inline_keyboard)


@dp.callback_query_handler(text_contains="apple")
async def buy_apple(call: CallbackQuery):
    await call.answer(cache_time=10)
    await call.message.answer(text='Apple chosen. Tap to see.', reply_markup=apple_keyboard)


@dp.callback_query_handler(purchase_callback.filter(item_name='peach'))
async def buy_peach(call: CallbackQuery, callback_data: dict):
    quantity = callback_data.get('quantity')
    await call.answer(cache_time=10)
    await call.message.answer(text=f'Peach chosen. {quantity} peaches left', reply_markup=peach_keyboard)


@dp.callback_query_handler(text='cancel')
async def cancel_purchase(call: CallbackQuery):
    await call.answer('Cancelled.', show_alert=True)
    await call.message.delete()
