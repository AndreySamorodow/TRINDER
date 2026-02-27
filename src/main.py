from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis

from src.core.redis import redis_manager
from src.auth import auth_router, oauth_router

from src.database.database import engine, Base
from src.config import settings

from src.auth.models import User
from src.profile.models import Profile, Preference

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    try:
        await redis_manager.connect()
        logger.info("Приложение запущено с Redis")
    except Exception as e:
        logger.error(f"Приложение запущено БЕЗ Redis: {e}")

    yield

    await redis_manager.disconnect()
    logger.info("Приложение остановлено")


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(oauth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
