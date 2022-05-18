from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

base_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/help',)]
], resize_keyboard=True, one_time_keyboard=True)

func_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='First Function')],
    [KeyboardButton(text='Second Function'), KeyboardButton(text='Third Function')]
], resize_keyboard=True, one_time_keyboard=True)

admin_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='ADD TEXT CMD')],
    [KeyboardButton(text='ADD MASTER')],
    [KeyboardButton(text='ADD SERVICE')],
    [KeyboardButton(text='CANCEL')]
],  resize_keyboard=True, one_time_keyboard=True)

request_phone_button_kbd = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Send my phone number", request_contact=True)],
], resize_keyboard=True, one_time_keyboard=True)
