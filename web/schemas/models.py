from pydantic import BaseModel,Field, field_validator
from typing import List


class GetUsers(BaseModel):
    user_id: int
    username: str
    fullname: str
    role: str
    ref: str

class TaskCreate(BaseModel):
    class_: int = Field(..., alias="class")  # Алиас для "class"
    trimester: int
    text: str
    correctAnswer: str  # Новое поле для правильного ответа


    @field_validator("class_")
    def validate_class(cls, value):
        if value not in range(5, 12):  # Диапазон 5-11
            raise ValueError("Класс должен быть от 5 до 11")
        return value

    @field_validator("trimester")
    def validate_trimester(cls, value):
        if value not in [1, 2, 3]:
            raise ValueError("Триместр должен быть 1, 2 или 3")
        return value

    @field_validator("text")
    def validate_text(cls, value):
        if not value.strip():
            raise ValueError("Текст задания не может быть пустым")
        return value

    @field_validator("correctAnswer")
    def validate_correct_answer(cls, value):
        if not value.strip():
            raise ValueError("Правильный ответ не может быть пустым")
        return value

class TasksRequest(BaseModel):
    tasks: List[TaskCreate]

class GetAnswers(BaseModel):
    taskId: int
    answer: str
