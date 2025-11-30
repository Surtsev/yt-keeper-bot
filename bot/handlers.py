import traceback

import httpx
from aiogram import Router, types
from aiogram.filters.command import Command

from config import URL

ALLOWED_USER_ID = {1378137303}

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.from_user.id not in ALLOWED_USER_ID:
        await message.answer("Доступ закрыт.")
        return
    await message.answer(
        """
        Основные команды:
        /add <URL> - добавить видео с ссылкой
        /delete <id> - удалить видео по его месту в твоём списке
        /list - показать все видео в твоём списке
        """
    )


@router.message(Command("delete"))
async def cmd_delete(message: types.Message):
    if message.from_user.id not in ALLOWED_USER_ID:
        await message.answer("Доступ закрыт.")
        return
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or len(args) > 2:
        await message.answer("Используйте /delete <id>")
        return
    video_id = int(args[1])
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{URL}/videos/{video_id}")
            print(f"Status: {response.status_code}")  # Добавь это
            print(f"Response: {response.text}")  # И это
            if response.status_code != 200:
                await message.answer(
                    f"❌ Ошибка {response.status_code}: {response.text}"
                )
                return
            data = response.json()
            await message.answer(f"✅ {data['message']}")
    except Exception:
        error_text = traceback.format_exc()
        with open("error.log", "a") as f:
            f.write(error_text + "\n\n")
        await message.answer("Произошла ошибка, подробности в лог-файле.")


@router.message(Command("add"))
async def cmd_add(message: types.Message):
    if message.from_user.id not in ALLOWED_USER_ID:
        await message.answer("Доступ закрыт.")
        return
    args = message.text.split(maxsplit=1)
    print(args)
    if len(args) < 2 or len(args) > 2:
        await message.answer("Используйте /add <URL>")
        return
    try:
        url = args[1]
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{URL}/videos", params={"url": url})
        data = response.json()
        await message.answer(f"✅ {data['message']}")
        # except Exception as e:
        # await message.answer(f"❌ Ошибка: {e}")
    except Exception:
        error_text = traceback.format_exc()
        with open("error.log", "w") as f:
            f.write(error_text)
        await message.answer("Произошла ошибка, подробности в лог-файле.")


@router.message(Command("list"))
async def cmd_list(message: types.Message):
    if message.from_user.id not in ALLOWED_USER_ID:
        await message.answer("Доступ закрыт.")
        return
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{URL}/videos")
            data = response.json()
        videos = data.get("videos", [])
        if not videos:
            await message.answer("Видео не найдены или не добавлен ни один.")
            return
        text = "Ваши видео\n"
        for video in videos:
            text += f"ID: {video['id']} - {video['url']}\n\n"
        await message.answer(text)
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
