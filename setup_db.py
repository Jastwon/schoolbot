import asyncio
from bot.core.orm import AsyncORM

async def main():
    await AsyncORM.create_tables()

if __name__ == "__main__":
    asyncio.run(main())