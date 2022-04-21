from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import purchase_callback
from settings import apple_url, peach_url

inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Buy apple", callback_data=purchase_callback.new(item_name='apple',
                                                                                   quantity=5)),
        InlineKeyboardButton(text="Buy peach", callback_data=purchase_callback.new(item_name='peach',
                                                                                   quantity=1))
    ],
    [InlineKeyboardButton(text="Cancel", callback_data='cancel')]
                                                        ])

apple_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Here", url=apple_url)]
                                                        ])

peach_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Here", url=peach_url)]
                                                        ])
