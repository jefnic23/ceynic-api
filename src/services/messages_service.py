from pathlib import Path
from typing import Annotated

from fastapi import Depends
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from src.config import Settings, get_settings


class MessagesService:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]):
        self._settings: Settings = settings

        # self.api_key = settings.MAILGUN_API_KEY
        # self.domain = settings.MAILGUN_DOMAIN
        # self.public_key = settings.MAILGUN_PUBLIC_KEY

    def get_fast_mail(self, from_name: str, from_email) -> FastMail:
        connection_config = self._get_connection_config(
            from_name=from_name, from_email=from_email
        )

        return FastMail(connection_config)

    def build_message(self, from_name: str, message: str) -> MessageSchema:
        return MessageSchema(
            subject=f"[TraceyNicholasArt] Message from {from_name}",
            recipients=[self._settings.RECIPIENT_EMAIL],
            template_body={"message": message},
            subtype=MessageType.html,
        )

    def _get_connection_config(
        self, from_name: str, from_email: str
    ) -> ConnectionConfig:
        return ConnectionConfig(
            MAIL_USERNAME=self._settings.MAILGUN_SMTP_LOGIN,
            MAIL_PASSWORD=self._settings.MAILGUN_SMTP_PASSWORD,
            MAIL_PORT=self._settings.MAILGUN_SMTP_PORT,
            MAIL_SERVER=self._settings.MAILGUN_SMTP_SERVER,
            MAIL_FROM=from_email,
            MAIL_FROM_NAME=from_name,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
            TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
        )
