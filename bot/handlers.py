import httpx
from aiogram import Router, types
from aiogram.filters.command import Command

from config import URL

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
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
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or len(args) > 2:
        await message.answer("Используйте /delete <id>")
        return
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{URL}/videos/{id}")
            data = response.json()
        await message.answer(f"✅ {data['message']}")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")


@router.message(Command("add"))
async def cmd_add(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or len(args) > 2:
        await message.answer("Используйте /add <URL>")
        return
    try:
        url = args[1]
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{URL}/videos", params={"url": url})
        data = response.json()
        await message.answer(f"✅ {data['message']}")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")


@router.message(Command("list"))
async def cmd_list(message: types.Message):
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
