from fastapi import FastAPI, Security, HTTPException, status, Depends, Request
from fastapi.security import APIKeyHeader
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from .teachers import teachers_router
from .students import students_router

from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from bot.core.orm import AsyncORM

from .schemas.models import GetUsers


from bot.config import TOKEN_MYAPI



app = FastAPI()
app.include_router(teachers_router, prefix="/teacher", tags=["teacher"])
app.include_router(students_router, prefix="/student", tags=["student"])







app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

API_KEY_NAME = "api-key"
api_key_scheme = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def validate_api_key(api_key: str = Security(api_key_scheme)):
    if api_key != TOKEN_MYAPI:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный API ключ",
        )
    return api_key




@app.get("/users", response_model=list[GetUsers])
async def get_users(api_key: str = Depends(validate_api_key)):
    return await AsyncORM.select_users()




@app.get("/teacher", response_class=HTMLResponse)
async def main_teacher(request: Request):
    return templates.TemplateResponse("teacher.html", {"request": request})

@app.get("/teachers")
async def get_teachers_name(student_id: int):
    return await AsyncORM.get_teachers_by_student(student_id)



async def start_web():
    config = uvicorn.Config(app, host="127.0.0.1", port=8000)
    server = uvicorn.Server(config)
    await server.serve()



