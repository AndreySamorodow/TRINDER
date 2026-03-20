import asyncio
import logging
import aiohttp

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, CommandObject
from config import settings

bot = Bot(token=settings.TG_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart(deep_link=True)) # deep_link=True ловит именно такие ссылки
async def handle_deep_link(message: types.Message, command: CommandObject):
    """
    Обрабатывает команду /start с параметром (например, /start abcd1234)
    """
    secret_code = command.args
    telegram_user_id = message.from_user.id

    if not secret_code:
        await message.answer("Добро пожаловать! Но чтобы привязать аккаунт, перейдите по ссылке с сайта.")
        return

    # Отправляем запрос в ваш FastAPI бэкенд
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"http://localhost:8000/api/profile/auth/telegram-bind",
            json={
                "telegram_id": telegram_user_id,
                "code": secret_code
            }
        ) as resp:
            if resp.status == 200:
                await message.answer("✅ Отлично! Ваш Telegram привязан к аккаунту.")
            elif resp.status == 404:
                await message.answer("⏰ Код привязки устарел или не найден. Запросите новую ссылку на сайте.")
            else:
                await message.answer("❌ Произошла ошибка. Попробуйте еще раз на сайте.")

@dp.message(CommandStart())
async def handle_start(message: types.Message):
    # Обычный /start без параметров
    await message.answer("Привет! Я бот для уведомлений.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())