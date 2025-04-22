from sqlalchemy import select
import asyncio

from bot.database import Base, async_engine, async_session_factory
from bot.models import Users, Tasks


class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.connect() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()

    @staticmethod
    async def insert_users(user_id: int, username: str, fullname: str, role: str, ref: str):
        async with async_session_factory() as session:
            user = Users(user_id=user_id, username=username, fullname = fullname, role=role, ref=ref)
            session.add(user)
            await session.flush()
            await session.commit()







    @staticmethod
    async def select_users():
        async with async_session_factory() as session:
            query = select(Users)
            res = await session.execute(query)
            users = res.scalars().all()
            return users


    @staticmethod
    async def update_username(user_id: int, new_username: str):
        async with async_session_factory() as session:
            user = await session.get(Users, user_id)
            user.username = new_username
            # await session.refresh(user)
            await session.commit()

    @staticmethod
    async def update_role(user_id: int, new_role: str = "teacher"):
        async with async_session_factory() as session:
            user = await session.get(Users, user_id)
            user.role = new_role
            # await session.refresh(user)
            await session.commit()


    @staticmethod
    async def get_user_by_id(user_id: int):
        async with async_session_factory() as session:
            query = select(Users).where(Users.user_id == user_id)
            res = await session.execute(query)
            try:
                users = res.one()
                return users[0]
            except:
                return None

    @staticmethod
    async def get_teachers_by_student(student_id: int):
        async with async_session_factory() as session:
            query = select(Users).where(Users.user_id == student_id)
            res = await session.execute(query)
            users = res.one()

            query = select(Users).where(Users.role == "teacher")
            res = await session.execute(query)
            all_teachers = res.scalars().all()
            teachers = list()

            for teacher in all_teachers:
                if str(teacher.id) in users[0].ref:
                    teachers.append(teacher)

            return teachers


    @staticmethod
    async def get_users_by_ref(ref: str):
        async with async_session_factory() as session:
            query = select(Users).where(Users.role == "student")
            res = await session.execute(query)
            all_students = res.scalars().all()
            students = list()
            for student in all_students:
                if ref in student.ref:
                    students.append(student)

            return students

    @staticmethod
    async def get_user_by_username(username: str):
        async with async_session_factory() as session:
            query = select(Users).where(Users.username == username)
            res = await session.execute(query)
            user = res.one()[0]
            return user

    @staticmethod
    async def add_ref(user_id:int, teacher_id: str):
        async with async_session_factory() as session:
            user = await session.get(Users, user_id)
            if not(teacher_id in user.ref):
                user.ref += f"{teacher_id} "
            await session.commit()

    @staticmethod
    async def delete_ref(user_id:int, teacher_id: str):
        async with async_session_factory() as session:
            user = await session.get(Users, user_id)
            user.ref = user.ref.replace(f"{teacher_id}", "")
            print(user.ref)
            await session.commit()

    @staticmethod
    async def insert_tasks(user_id: int, correct_answer: str, data):
        async with async_session_factory() as session:
            new_task = Tasks(
                user_id=user_id,
                text=data['task_text'],
                age=data['age'],
                period=data['period'],
                correct_answer=correct_answer,  # Сохраняем правильный ответ
            )
            session.add(new_task)
            await session.commit()

    @staticmethod
    async def get_tasks_by_id(teacher_id: int, age: str, period: str):
        async with async_session_factory() as session:
            query = select(Tasks).filter_by(user_id=teacher_id, age=age, period=period)
            res = await session.execute(query)
            tasks = res.scalars().all()
            return tasks






