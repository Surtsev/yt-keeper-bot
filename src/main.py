import asyncio
from threading import Thread

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from api.routes import api as fastapi_app
from bot.handlers import router
from config import BOT_TOKEN


def run_fastapi():
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)


async def run_aiogram():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    commands = [
        BotCommand(command="start", description="Начать работу"),
        BotCommand(command="add", description="Добавить видео"),
        BotCommand(command="delete", description="Удалить видео"),
        BotCommand(
            command="list", description="Показать список всех добавленных видео"
        ),
    ]
    await bot.set_my_commands(commands)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def main():
    fastapi_thread = Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()

    await run_aiogram()


if __name__ == "__main__":
    asyncio.run(main())
