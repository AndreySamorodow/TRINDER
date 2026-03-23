from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisDB(BaseModel):
    cache: int = 0

class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: RedisDB = RedisDB()

class CacheNamespace(BaseModel):
    users_list: str = "users-list"
    profiles_list: str = "profiles_list"

class CacheConfig(BaseModel):
    prefix: str = "fastapi-cache"
    namespace: CacheNamespace = CacheNamespace()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


    DATABASE_URL: str
    REDIS_URL: str

    OAUTH_GOOGLE_CLIENT_ID: str
    OAUTH_GOOGLE_CLIENT_SECRET: str

    #JWT
    SECRET_KEY: str
    ALGORITHM: str

    #S3
    S3_ACCESS_KEY:str
    S3_SECRET_KEY:str
    S3_BUCKET_NAME: str
    S3_DOMEN: str
    redis: RedisConfig = RedisConfig()
    cache: CacheConfig = CacheConfig()
    
    


settings = Settings()
