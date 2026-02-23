from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    OAUTH_GOOGLE_CLIENT_ID: str
    OAUTH_GOOGLE_CLIENT_SECRET: str

    class Config:
        env_file = ".env"

settings = Settings()