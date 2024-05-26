from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    MAILGUN_SMTP_SERVER: str
    MAILGUN_SMTP_PORT: int
    MAILGUN_SMTP_LOGIN: str
    MAILGUN_SMTP_PASSWORD: str
    MAILGUN_API_KEY: str
    MAILGUN_DOMAIN: str
    MAILGUN_PUBLIC_KEY: str
    EMAIL_RECIPIENT: str
    BUCKETEER_AWS_ACCESS_KEY_ID: str
    BUCKETEER_AWS_REGION: str
    BUCKETEER_AWS_SECRET_ACCESS_KEY: str
    BUCKETEER_BUCKET_NAME: str
    PAYPAL_CLIENT_ID: str
    PAYPAL_CLIENT_SECRET: str
    RECAPTCHA_SITE_KEY: str
    RECAPTCHA_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    return Settings()


SETTINGS_DEPENDENCY = Annotated[Settings, Depends(get_settings)]
