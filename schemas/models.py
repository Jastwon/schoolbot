from pydantic import BaseModel

class GetUsers(BaseModel):
    user_id: int
    username: str
    fullname: str
    role: str
    ref: str