from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminStates(StatesGroup):
    admin_state = State()
