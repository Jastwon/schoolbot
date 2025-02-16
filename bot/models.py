from sqlalchemy import Integer, String

<<<<<<< HEAD
from .database import Base
=======
from bot.database import Base
>>>>>>> fa75e18 (Сделал запуск тг бота и веб апп из одного файла)
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
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[str] = mapped_column(String, nullable=False)
    period: Mapped[str] = mapped_column(String, nullable=False)
