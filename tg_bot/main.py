import asyncio
import json
import logging
import aiohttp

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, CommandObject
from aiokafka import AIOKafkaConsumer
from config import settings

bot = Bot(token=settings.TG_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

async def send_to_user(user_id: int, text: str):
    try:
        await bot.send_message(chat_id=user_id, text=text)
        print(f"Сообщение отправлено пользователю {user_id}")
    except Exception as e:
        print(f"Ошибка отправки: {e}")

async def consume_notifications():
    consumer = AIOKafkaConsumer(
        "notifications",
        bootstrap_servers="localhost:9092",
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    await consumer.start()
    try:
        logger.info("Kafka Consumer started. Listening for messages...")
        async for msg in consumer:
            notification_data = msg.value
            if notification_data["type"] == "tg":
                 await send_to_user(user_id=notification_data["recipient"], text=notification_data["body"])

    finally:
        await consumer.stop()


async def main():
    polling_task = asyncio.create_task(dp.start_polling(bot))
    consumer_task = asyncio.create_task(consume_notifications())
    
    await asyncio.gather(polling_task, consumer_task)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
