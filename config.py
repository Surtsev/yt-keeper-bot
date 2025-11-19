import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN is None:
    raise ValueError("Не найден токен бота")
URL = os.getenv("URL")
if URL is None:
    raise ValueError("Не найден url сервера")
