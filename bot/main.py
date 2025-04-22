from gettext import textdomain

from bot.config import *
import logging
import json

from aiogram.utils.executor import start_polling
from aiogram import Bot
from aiogram.types import Message, ChatActions, CallbackQuery, ReplyKeyboardRemove, WebAppInfo, ContentType
from aiogram.dispatcher import Dispatcher, FSMContext, filters
from aiogram.utils.deep_linking import get_start_link
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from bot.keyboards import *
from bot.states import *

from datetime import datetime

from bot.core.orm import AsyncORM






logging.basicConfig(level=logging.INFO)
memory = MemoryStorage()
bot = Bot(token=TOKEN)
disp = Dispatcher(bot, storage=memory)
BASE_DOMAIN = "z8xc7a-46-138-24-156.ru.tuna.am"



@disp.message_handler(commands=["start"])
async def start(message: Message):
    global args
    args = message.get_args()


    # await AsyncORM.create_tables()

    user = await AsyncORM.get_user_by_id(message.from_user.id)
    if user == None:
        await bot.send_message(message.from_user.id, "Введите имя")
        await Fullname.first_name.set()
    else:
        if user.username != message.from_user.username:
            await AsyncORM.update_username(message.from_user.id, message.from_user.username)
        if args != "" and args != str(message.from_user.id):
            await AsyncORM.add_ref(message.from_user.id, args)
            await bot.send_message(int(args), "У вас новый ученик")

        if user.role == "student":
            await bot.send_message(message.from_user.id, "меню", reply_markup=student_menu())
            keyboard = InlineKeyboardMarkup()
            button = InlineKeyboardButton(
                text="Открыть веб-приложение",
                web_app=WebAppInfo(
                    url=f"https://{BASE_DOMAIN}/student/my_teachers?student_id={message.from_user.id}")
            )
            keyboard.add(button)
            await message.answer("Веб апп", reply_markup=keyboard)
        else:
            await bot.send_message(message.from_user.id, "главное меню", reply_markup=teacher_menu())
            keyboard = InlineKeyboardMarkup()
            button = InlineKeyboardButton(
                text="Открыть веб-приложение",
                web_app=WebAppInfo(
                    url=f"https://{BASE_DOMAIN}/teacher")
            )
            keyboard.add(button)
            await message.answer("Веб апп", reply_markup=keyboard)


@disp.message_handler(commands=["admin"])
async def admin(msg: Message):
    if msg.from_user.id in ADMIN:
        await bot.send_message(msg.from_user.id, "Админ меню", reply_markup=admin_menu())


@disp.message_handler()
async def messages(message: Message):
    global msgg


    if message.text == "Рассылка" and message.from_user.id in ADMIN:
        await bot.send_message(message.from_user.id, "Рассылка")
    elif message.text == "Управление пользователем" and message.from_user.id in ADMIN:
        await bot.send_message(message.from_user.id, "Введите юзернейм пользователя")
        await ManageUser.user.set()
    elif message.text == "Статистика" and message.from_user.id in ADMIN:
        await bot.send_message(message.from_user.id, "Статистика")
        users = await AsyncORM.select_users()
        for user in users:
            print(user.ref)

    user = await AsyncORM.get_user_by_id(message.from_user.id)
    if user.role == "teacher":
        if message.text == "Мои ученики":
            students = await AsyncORM.get_users_by_ref(str(message.from_user.id))
            if students == []:
                await bot.send_message(message.from_user.id, "У вас нет учеников")

            else:
                for student in students:
                    msgg = await bot.send_message(message.from_user.id, f"{student.fullname}\nТелеграм: @{student.username}", reply_markup=my_students(student.user_id))
        elif message.text == "Моя ссылка":
            await bot.send_message(message.from_user.id, f"Отправьте ссылку ученику\n`{await get_start_link(str(message.from_user.id))}`", parse_mode="MARKDOWN")

        elif message.text == "Мои задания":
            await bot.send_message(message.from_user.id, "Введите класс учеников (например: 5):")
            await TeacherStates.waiting_age.set()
    else:
        if message.text == "Мои учителя":
            teachers_id = user.ref.split()
            teachers = list()
            for teacher_id in teachers_id:
                teachers.append(await AsyncORM.get_user_by_id(int(teacher_id)))
            await bot.send_message(message.from_user.id, "Выберите учителя", reply_markup=teachers_btn(teachers))










@disp.callback_query_handler(lambda call: call.data.startswith("myteacher_"))
async def my_teacher_select(call: CallbackQuery):
    global user_id_teacher
    user_id_teacher = int(call.data.split("_")[1])
    await bot.send_message(call.from_user.id, "Введите класс (только число)")
    await GetTasks.age.set()


@disp.callback_query_handler(lambda call: call.data.startswith("changerole_"))
async def mng(call: CallbackQuery):
    global user_data

    user_id = int(call.data.split("_")[1])
    user = await AsyncORM.get_user_by_id(user_id)

    if user != "":
        if user.role == "student":
            await AsyncORM.update_role(user_id=user_id)
            await bot.edit_message_text(f"Пользователь: @{user.username}\nИмя: {user.fullname}\nРоль: teacher",
                                        call.from_user.id, user_data.message_id, reply_markup=mng_user(user_id))
            await bot.send_message(user_id, "ваша роль изменена на teacher")

        else:
            await AsyncORM.update_role(user_id=user_id, new_role="student")
            await bot.edit_message_text(f"Пользователь: @{user.username}\nИмя: {user.fullname}\nРоль: student",
                                        call.from_user.id, user_data.message_id, reply_markup=mng_user(user_id))
            await bot.send_message(user_id, "ваша роль изменена на student")


@disp.callback_query_handler(lambda call: call.data.startswith("mystudent_"))
async def mystd(call: CallbackQuery):
    pass


@disp.callback_query_handler(lambda call: call.data.startswith("deletestudent_"))
async def delete_student(call: CallbackQuery):
    student_id = call.data.split("_")[1]
    await AsyncORM.delete_ref(int(student_id), str(call.from_user.id))
    await bot.delete_message(call.from_user.id, msgg.message_id)
    await bot.send_message(call.from_user.id, "Ученик удален")


@disp.callback_query_handler(text="again")
async def again(call: CallbackQuery):
    global msg_true
    await bot.send_message(call.from_user.id, "Введите имя")
    await bot.delete_message(call.from_user.id, msg_true.message_id)
    await Fullname.first_name.set()


@disp.callback_query_handler(text="next")
async def next(call: CallbackQuery):
    await AsyncORM.insert_users(call.from_user.id, call.from_user.username, first_n + " " + second_n, "student",
                                f"{args} ")
    if args != "":
        await bot.send_message(int(args), "У вас новый ученик")
    await bot.send_message(call.from_user.id, "меню", reply_markup=student_menu())












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

    user = ""
    try:
        user = await AsyncORM.get_user_by_username(msg.text)

        user_data = await bot.send_message(msg.from_user.id, f"Пользователь: @{user.username}\nИмя: {user.fullname}\nРоль: {user.role}", reply_markup=mng_user(user.user_id))
        await state.finish()

    except:
        await bot.send_message(msg.from_user.id, "Пользователь не найден")





@disp.message_handler(state=TeacherStates.waiting_age)
async def process_age(message: Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 11:
        await state.update_data(age=message.text)
        await TeacherStates.next()
        await message.answer("Введите номер триместра (1-3):", reply_markup=trimester_keyboard())
    else:
        await message.answer("Некорректный класс! Введите число от 1 до 11:")

@disp.message_handler(state=TeacherStates.waiting_period)
async def process_period(message: Message, state: FSMContext):
    if message.text in ["1", "2", "3"]:
        await state.update_data(period=message.text)
        await TeacherStates.next()
        await message.answer("Введите текст задания:", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Используйте кнопки для выбора триместра!")

@disp.message_handler(state=TeacherStates.waiting_task_text)
async def process_task_text(message: Message, state: FSMContext):
    await state.update_data(task_text=message.text)
    await TeacherStates.next()
    await message.answer("Введите правильный ответ на это задание:")

# Новый обработчик для правильного ответа
@disp.message_handler(state=TeacherStates.waiting_correct_answer)
async def process_correct_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    
    await AsyncORM.insert_tasks(message, data)
    
    await state.finish()
    await message.answer("✅ Задание и ответ успешно сохранены!", reply_markup=teacher_menu())





@disp.message_handler(state=GetTasks.age)
async def get_age(msg: Message, state: FSMContext):
    await state.update_data(age=msg.text)
    await GetTasks.next()
    await msg.answer("Введите триместр", reply_markup=trimester_keyboard())

@disp.message_handler(state=GetTasks.period)
async def get_period(msg: Message, state: FSMContext):
    data = await state.get_data()
    period = msg.text
    tasks = await AsyncORM.get_tasks_by_id(user_id_teacher, data["age"], period)
    if not(tasks):
        await msg.answer("Для вас нет заданий", reply_markup=student_menu())
        await state.finish()
        return
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(
        text="Открыть веб-приложение",
        web_app=WebAppInfo(url=f"https://k8y3y5-46-138-24-156.ru.tuna.am/webapp?teacher_id={user_id_teacher}&age={data['age']}&period={period}")
    )
    keyboard.add(button)
    await msg.answer("Для выполнения откройте приложение", reply_markup=keyboard)
    await state.finish()

#send web_app
























def start_bot():
    start_polling(disp, skip_updates=True)