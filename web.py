from fastapi import FastAPI, Security, HTTPException, status, Depends, Request
from fastapi.security import APIKeyHeader
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from bot.core.orm import AsyncORM
from schemas.models import GetUsers

import uvicorn


from bot.config import TOKEN_MYAPI



app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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

@app.post()

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse("get_users.html", {"request": request})


async def start_web():
    config = uvicorn.Config(app, host="localhost", port=8000)
    server = uvicorn.Server(config)
    await server.serve()





