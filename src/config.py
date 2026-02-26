from pydantic import BaseModel
from pydantic_settings import BaseSettings


class RedisDB(BaseModel):
    cache: int = 0


class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: RedisDB = RedisDB()


class CacheNamespace(BaseModel):
    oauth_state_list: str = "oauth_state_list"


class CacheConfig(BaseModel):
    prefix: str = "fastapi-cache"
    namespace: CacheNamespace = CacheNamespace()



class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str

    OAUTH_GOOGLE_CLIENT_ID: str
    OAUTH_GOOGLE_CLIENT_SECRET: str

    #JWT
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"


    redis:RedisConfig = RedisConfig()
    cache:CacheConfig = CacheConfig()

settings = Settings()
