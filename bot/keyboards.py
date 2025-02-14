from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

def back():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("Отмена")
    kb.add(btn)
    return kb

def input_again():
    kb = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("Ввести заново", callback_data="again")
    btn2 = InlineKeyboardButton("Все верно", callback_data="next")
    kb.add(btn, btn2)
    return kb


def admin_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Рассылка")
    btn2 = KeyboardButton("Управление пользователем")
    btn3 = KeyboardButton("Статистика")
    kb.add(btn1, btn2, btn3)
    return kb

def mng_user(user_id: int):
    kb = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("изменить роль", callback_data=f"changerole_{user_id}")
    # btn2 = InlineKeyboardButton("Все верно", callback_data="next")
    kb.add(btn)
    return kb


def teacher_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Мои ученики")
    btn2 = KeyboardButton("Мои задания")
    btn3 = KeyboardButton("Моя ссылка")
    kb.add(btn1, btn2, btn3)
    return kb


def student_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Мои учителя")
    kb.add(btn1)
    return kb

def teachers_btn(teachers: list):
    kb = InlineKeyboardMarkup()
    for teacher in teachers:
        btn = InlineKeyboardButton(teacher.fullname, callback_data=f"myteacher_{teacher.user_id}")
        kb.add(btn)
    return kb




def my_students(user_id: int):
    kb = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("задать задание", callback_data=f"mystudent_{user_id}")
    btn2 = InlineKeyboardButton("Удалить ученика", callback_data=f"deletestudent_{user_id}")
    kb.add(btn, btn2)
    return kb

