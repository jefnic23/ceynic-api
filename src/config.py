from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BUNNY_API_KEY: str
    BUNNY_PULL_ZONE_HOSTNAME: str
    BUNNY_STORAGE_ZONE_NAME: str
    BUNNY_STORAGE_ZONE_PASSWORD: str
    BUNNY_STORAGE_ZONE_REGION: str
    DATABASE_URL: str
    FASTAPI_ENV: str = "production"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    MAILGUN_SMTP_SERVER: str
    MAILGUN_SMTP_PORT: int
    MAILGUN_SMTP_LOGIN: str
    MAILGUN_SMTP_PASSWORD: str
    MAILGUN_API_KEY: str
    MAILGUN_DOMAIN: str
    MAILGUN_PUBLIC_KEY: str
    RECIPIENT_EMAIL: str
    PAYPAL_BASE_URL: str
    RECAPTCHA_SECRET_KEY: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
