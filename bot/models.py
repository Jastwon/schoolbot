from sqlalchemy import Integer, String

from bot.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    fullname: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)
    ref: Mapped[str] = mapped_column(String)


class Tasks(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(String)
    age: Mapped[str] = mapped_column(String)
    period: Mapped[str] = mapped_column(String)
    correct_answer: Mapped[str] = mapped_column(String)  # Новое поле