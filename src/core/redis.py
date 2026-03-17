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
    
    async def start(self):
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
                logger.info("Redis connected")
            except Exception as e:
                logger.error(f"Error Redis: {e}")
                raise
    
    async def stop(self):
        if self._redis:
            await self._redis.close()
        if self._pool:
            await self._pool.disconnect()
        self._initialized = False
        logger.info("Redis disconnected")
    
    @property
    def client(self) -> Redis:
        if not self._initialized or self._redis is None:
            raise RuntimeError("Redis is not initialized. Call connect() in lifespan")
        return self._redis
    
    @property
    def is_connected(self) -> bool:
        return self._initialized and self._redis is not None

redis_manager = RedisManager()

async def get_redis():
    if not redis_manager.is_connected:
        raise HTTPException(
            status_code=503,
            detail="Redis service is temporarily unavailable. Please try again later."
        )
    
    try:
        await redis_manager.client.ping()
        return redis_manager.client
    except Exception as e:
        logger.error(f"Error while receiving Redis client: {e}")
        raise HTTPException(
            status_code=503,
            detail="Redis service is unavailable"
        )

RedisSession = Annotated[Redis, Depends(get_redis)]
