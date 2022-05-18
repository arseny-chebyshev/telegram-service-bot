from aiogram.dispatcher.filters.state import StatesGroup, State


class ServiceDialog(StatesGroup):
    select_service = State()
    select_master = State()
    select_schedule = State()
    select_hour = State()


class RegisterUser(StatesGroup):
    send_contact = State()
