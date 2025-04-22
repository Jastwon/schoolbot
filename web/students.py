from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from bot.core.orm import AsyncORM
from bot.database import async_session_factory
from bot.models import Users


from sqlalchemy import select

from web.schemas.models import GetAnswers

students_router = APIRouter()
templates = Jinja2Templates(directory="web/templates")


@students_router.get("/my_teachers", response_class=HTMLResponse)
async def get_my_teachers(student_id: int, request: Request):
    init_data = request.query_params.get("user")
    print(init_data)
    # if not init_data:
    #     raise HTTPException(status_code=400)

    async with async_session_factory() as session:
        query = select(Users).where(Users.user_id == student_id)
        res = await session.execute(query)
        user = res.one()[0]
        teachers_id = user.ref.split()
        teachers = list()
        for teacher_id in teachers_id:
            query = select(Users).where(Users.user_id == int(teacher_id))
            res = await session.execute(query)
            teachers.append(res.one()[0])

        return templates.TemplateResponse("mytasks.html", {"request": request, "teachers": teachers})


@students_router.get("/get_tasks")
async def get_tasks(teacher: int, class_: str, trimester: str):
    return await AsyncORM.get_tasks_by_id(teacher, class_, trimester)

@students_router.post("/answers")
async def answers(answers: list[GetAnswers]):
    print(answers)





