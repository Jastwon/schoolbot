import threading
import asyncio

from bot.main import start_bot
from web import start_web

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot())


def run_web_app():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_web())

if __name__ == "__main__":
    # Создаем потоки для бота и веб-приложения
    bot_thread = threading.Thread(target=run_bot)
    #web_app_thread = threading.Thread(target=run_web_app)

    # Запускаем потоки
    bot_thread.start()
    #web_app_thread.start()

    # Ждем завершения потоков (хотя они могут работать бесконечно)
    bot_thread.join()
    #web_app_thread.join()