from sqlalchemy import Integer, String

from database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    fullname: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)
    ref: Mapped[str] = mapped_column(String)

