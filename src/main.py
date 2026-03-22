from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis

from src.core.redis import redis_manager
from src.core.kafka import kafka_producer
from src.core.scheduler import start_scheduler, stop_scheduler

from src.auth import auth_router, oauth_router
from src.profile import profile_router, preference_router
from src.swipe import swipe_router

from src.database.database import engine, Base
from src.config import settings

from src.auth.models import User
from src.profile.models import Profile
from src.profile.preference.models import Preference
from src.swipe.models import Swipe

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    await redis_manager.start()
    await kafka_producer.start()
    start_scheduler()

    yield

    stop_scheduler()
    await kafka_producer.stop()
    await redis_manager.stop()

    logger.info("App is stopped")


app = FastAPI(title="TRINDER", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(oauth_router)
app.include_router(profile_router)
app.include_router(preference_router)
app.include_router(swipe_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from src.core.scheduler import build_decks_job

@app.post("/test-build-decks")
async def manual_build():
    await build_decks_job()
    return {"status": "done"}