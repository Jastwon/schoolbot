from aiogram.dispatcher.filters.state import State, StatesGroup

class Fullname(StatesGroup):
    first_name = State()
    second_name = State()

class ManageUser(StatesGroup):
    user = State()

class TeacherStates(StatesGroup):
    waiting_age = State()
    waiting_period = State()
    waiting_task_text = State()
    waiting_correct_answer = State()