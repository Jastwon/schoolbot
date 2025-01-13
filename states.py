from aiogram.dispatcher.filters.state import State, StatesGroup

class Fullname(StatesGroup):
    first_name = State()
    second_name = State()

class ManageUser(StatesGroup):
    user = State()