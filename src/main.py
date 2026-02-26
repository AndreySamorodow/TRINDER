from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis

from src.auth import auth_router, oauth_router

from src.database.database import engine, Base
from src.auth.models import User
from src.profile.models import Profile, Preference
from src.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db = settings.redis.db.cache
    )
    FastAPICache.init(
        RedisBackend(redis),
        prefix=settings.cache.prefix
    )
    yield

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
