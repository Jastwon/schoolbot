from fastapi import FastAPI, Security, HTTPException, status, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

from bot.core.orm import AsyncORM
from .schemas.models import GetUsers


from bot.config import TOKEN_MYAPI



app = FastAPI()

API_KEY_NAME = "x-api-key"
api_key_scheme = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def validate_api_key(api_key: str = Security(api_key_scheme)):
    if api_key != TOKEN_MYAPI:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный API ключ",
        )
    return api_key



class Test(BaseModel):
    key: str

@app.post("/users", response_model=list[GetUsers])
async def get_users(testt: Test, api_key: str = Depends(validate_api_key)):
    return await AsyncORM.select_users()




