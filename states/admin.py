from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminStates(StatesGroup):
    admin_state = State()


class ServiceMultiselect(StatesGroup):
    inserting_master = State()


class MasterMultiselect(StatesGroup):
    inserting_price = State()
    inserting_service = State()
