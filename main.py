from gettext import textdomain

from config import TOKEN, ADMIN
import logging

from aiogram.utils.executor import start_polling
from aiogram import Bot
from aiogram.types import Message, ChatActions, CallbackQuery
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils.deep_linking import get_start_link
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from keyboards import input_again, admin_menu, back, mng_user, teacher_menu
from states import Fullname, ManageUser

from datetime import datetime

from core.orm import AsyncORM






logging.basicConfig(level=logging.INFO)
memory = MemoryStorage()
bot = Bot(token=TOKEN)
disp = Dispatcher(bot, storage=memory)




@disp.message_handler(commands=["start"])
async def start(message: Message):
    global args
    args = message.get_args()
    await AsyncORM.create_tables()

    user = await AsyncORM.get_user_by_id(message.from_user.id)
    if user == None:
        await bot.send_message(message.from_user.id, "Введите имя")
        await Fullname.first_name.set()
    else:
        if user.username != message.from_user.username:
            await AsyncORM.update_username(message.from_user.id, message.from_user.username)
        if user.role == "student":
            await bot.send_message(message.from_user.id, "меню")
        else:
            await bot.send_message(message.from_user.id, "главное меню", reply_markup=teacher_menu())


@disp.message_handler(commands=["admin"])
async def admin(msg: Message):
    if msg.from_user.id in ADMIN:
        await bot.send_message(msg.from_user.id, "Админ меню", reply_markup=admin_menu())


@disp.message_handler()
async def messages(message: Message):
    if message.text == "Рассылка" and message.from_user.id in ADMIN:
        await bot.send_message(message.from_user.id, "Рассылка")
    elif message.text == "Управление пользователем" and message.from_user.id in ADMIN:
        await bot.send_message(message.from_user.id, "Введите юзернейм пользователя", reply_markup=back())
        await ManageUser.user.set()
    elif message.text == "Управление пользователем" and message.from_user.id in ADMIN:
        await bot.send_message(message.from_user.id, "Статистика")











@disp.message_handler(state=Fullname.first_name)
async def first_name(message: Message, state: FSMContext):
    global first_n
    first_n = message.text
    await bot.send_message(message.from_user.id, "Введите фамилию")
    await Fullname.next()

@disp.message_handler(state=Fullname.second_name)
async def second_name(message: Message, state: FSMContext):
    global second_n
    global msg_true
    second_n = message.text
    msg_true = await bot.send_message(message.from_user.id, f"Все правильно?\n{first_n} {second_n}", reply_markup=input_again())
    await state.finish()

@disp.message_handler(state=ManageUser.user)
async def manage_user(msg: Message, state: FSMContext):
    global user_data

    if msg.text == "Отмена":
        await bot.send_message(msg.from_user.id, "Админ меню", reply_markup=admin_menu())
        await state.finish()
    else:
        user = ""
        try:
            user = await AsyncORM.get_user_by_username(msg.text)

            user_data = await bot.send_message(msg.from_user.id, f"Пользователь: @{user.username}\nИмя: {user.fullname}\nРоль: {user.role}", reply_markup=mng_user(user.user_id))
            await state.finish()

        except:
            await bot.send_message(msg.from_user.id, "Пользователь не найден")




@disp.callback_query_handler(lambda call: call.data.startswith("changerole_"))
async def mng(call: CallbackQuery):
    global user_data

    user_id = int(call.data.split("_")[1])
    user = await AsyncORM.get_user_by_id(user_id)


    if user != "":
        if user.role == "student":
            await AsyncORM.update_role(user_id=user_id)
            await bot.edit_message_text(f"Пользователь: @{user.username}\nИмя: {user.fullname}\nРоль: teacher", call.from_user.id, user_data.message_id, reply_markup=mng_user(user_id))
            await bot.send_message(user_id, "ваша роль изменена на teacher")

        else:
            await AsyncORM.update_role(user_id=user_id, new_role="student")
            await bot.edit_message_text(f"Пользователь: @{user.username}\nИмя: {user.fullname}\nРоль: student", call.from_user.id, user_data.message_id, reply_markup=mng_user(user_id))
            await bot.send_message(user_id, "ваша роль изменена на student")







@disp.callback_query_handler(text="again")
async def again(call: CallbackQuery):
    global msg_true
    await bot.send_message(call.from_user.id, "Введите имя")
    await bot.delete_message(call.from_user.id, msg_true.message_id)
    await Fullname.first_name.set()



@disp.callback_query_handler(text="next")
async def next(call: CallbackQuery):
    await AsyncORM.insert_users(call.from_user.id, call.from_user.username, first_n + " " + second_n, "student", args)
    await bot.send_message(call.from_user.id, "меню")

























if __name__ == "__main__":
    start_polling(disp, skip_updates=True)