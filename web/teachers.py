from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from bot.core.orm import AsyncORM
from web.schemas.models import TasksRequest

teachers_router = APIRouter()
templates = Jinja2Templates(directory="web/templates")





@teachers_router.get("/my_students", response_class=HTMLResponse)
async def get_my_students(teacher_id: str, request: Request):
    init_data = request.query_params.get("user")
    if not init_data:
        raise HTTPException(status_code=400)
    students = await AsyncORM.get_users_by_ref(teacher_id)
    return templates.TemplateResponse("get_mystudents.html", {"request": request, "students": students})

@teachers_router.get("/send_tasks", response_class=HTMLResponse)
async def send_tasks(request: Request):
    init_data = request.query_params.get("user")
    if not init_data:
        raise HTTPException(status_code=400)
    return templates.TemplateResponse("send_tasks.html", {"request": request})



@teachers_router.post("/tasks")
async def receive_tasks(tasks: TasksRequest, teacher_id: int):
    try:
        for task in tasks:
            print(task)
            await AsyncORM.insert_tasks(
                data={
                    "age": str(task.class_),
                    "period": str(task.trimester),
                    "task_text": task.text,
                },
                user_id=teacher_id,
                correct_answer=task.correctAnswer  # Передаем правильный ответ
            )
            return {"message": "Задания успешно сохранены"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении: {str(e)}")
