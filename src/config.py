from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
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

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
