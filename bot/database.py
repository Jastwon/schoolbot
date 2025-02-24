from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase



async_engine = create_async_engine(
    url = "sqlite+aiosqlite:////media/jastwon/c30d0ee5-e0d6-4b66-8efe-c6523a401730/python_project/projects/schoolbot-main/app/bot/core/database.db",
    echo = False
)

async_session_factory = async_sessionmaker(async_engine)



class Base(DeclarativeBase):
    pass









