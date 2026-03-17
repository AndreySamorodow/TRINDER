import asyncio
import json
import logging
from aiogram import Dispatcher, Bot
from aiokafka import AIOKafkaConsumer

from config import TOKEN_TG_BOT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


bot = Bot(TOKEN_TG_BOT)
dp = Dispatcher()


async def consume_notifications():
    consumer = AIOKafkaConsumer(
        "tg_notifications",
        bootstrap_servers="localhost:9092",
        group_id="notification-service-group",  # Важно для масштабирования
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    await consumer.start()
    try:
        logger.info("Kafka Consumer started. Listening for messages...")
        async for msg in consumer:
            # msg.value — это наше уведомление в виде словаря
            notification_data = msg.value
            logger.info(f"Received notification: {notification_data}")

            # Тут твоя логика отправки:
            # if notification_data["type"] == "email":
            #     await send_email(notification_data)
            # elif notification_data["type"] == "telegram":
            #     await send_telegram(notification_data)

            # Если не включен auto_commit, нужно коммитить вручную:
            # await consumer.commit()
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_notifications())