import json
import logging
from aiokafka import AIOKafkaProducer

logger = logging.getLogger(__name__)

class KafkaProducer:
    def __init__(self):
        self.bootstrap_servers: str = "localhost:9092"
        self.producer = None


    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Сериализуем в JSON
        )
        await self.producer.start()
        logger.info("Kafka Producer started")

    async def stop(self):
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka Producer stopped")


    async def send(self, topic: str, message: dict):
        try:
            await self.producer.send(topic, value=message)
            logger.info(f"Message sent to {topic}: {message}")
        except Exception as e:
            logger.error(f"Failed to send message: {e}")

kafka_producer = KafkaProducer()