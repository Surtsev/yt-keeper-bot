import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN is None:
    raise ValueError("Не найден токен бота")
URL = os.getenv("URL")
if URL is None:
    raise ValueError("Не найден URL сервера")
DB_URL = os.getenv("DB_URL")
if DB_URL is None:
    raise ValueError("Не найден URL базы данных")
