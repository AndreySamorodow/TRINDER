from redis.asyncio import Redis, ConnectionPool
from typing import Optional, Annotated
import logging
from fastapi import Depends, HTTPException

from src.config import settings

logger = logging.getLogger(__name__)

class RedisManager:
    
    def __init__(self):
        self._pool: Optional[ConnectionPool] = None
        self._redis: Optional[Redis] = None
        self._initialized = False
    
    async def connect(self):
        """Подключение к Redis"""
        if not self._initialized:
            try:
                self._pool = ConnectionPool.from_url(
                    settings.REDIS_URL,
                    max_connections=10,
                    decode_responses=True
                )
                self._redis = Redis(connection_pool=self._pool)
                await self._redis.ping()
                self._initialized = True
                logger.info("Redis подключен")
            except Exception as e:
                logger.error(f"Ошибка подключения к Redis: {e}")
                raise
    
    async def disconnect(self):
        """Отключение от Redis"""
        if self._redis:
            await self._redis.close()
        if self._pool:
            await self._pool.disconnect()
        self._initialized = False
        logger.info("🔌 Redis отключен")
    
    @property
    def client(self) -> Redis:
        """Получить клиент Redis"""
        if not self._initialized or self._redis is None:
            raise RuntimeError("Redis не инициализирован. Вызовите connect() в lifespan")
        return self._redis
    
    @property
    def is_connected(self) -> bool:
        """Проверить, подключен ли Redis"""
        return self._initialized and self._redis is not None

# Создаем глобальный экземпляр менеджера
redis_manager = RedisManager()

# Функция зависимости для FastAPI
async def get_redis():
    """
    Зависимость для получения Redis клиента.
    Используйте: redis: RedisSession
    """
    if not redis_manager.is_connected:
        # Вместо RuntimeError возвращаем понятную ошибку
        raise HTTPException(
            status_code=503,
            detail="Redis сервис временно недоступен. Попробуйте позже."
        )
    
    try:
        # Проверяем, что соединение живо
        await redis_manager.client.ping()
        return redis_manager.client
    except Exception as e:
        logger.error(f"Ошибка при получении Redis клиента: {e}")
        raise HTTPException(
            status_code=503,
            detail="Redis сервис недоступен"
        )

# Создаем тип для аннотации

RedisSession = Annotated[Redis, Depends(get_redis)]