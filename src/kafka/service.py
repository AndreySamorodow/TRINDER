from src.core.kafka import kafka_producer


class KafkaService:
    def __init__(self):
        self.kafka_producer = kafka_producer

    async def notify_swipe(self, user_tg_id_recipient: int, username: str):
        notification = {
            "type": "tg",
            "recipient": user_tg_id_recipient,
            "body": f"Тебя свайпнули) --> ❤️{username}❤️"
        }
        await self.kafka_producer.send("notifications", notification)

    async def notify_match(self, user_tg_id_recipient: int, username: str):
        notification = {
            "type": "tg",
            "recipient": user_tg_id_recipient,
            "body": f"У тебя мэтч с {username}❤️"
        }
        await self.kafka_producer.send("notifications", notification)