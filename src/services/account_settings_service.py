from sqlmodel import select

from src.database import ASYNC_SESSION_DEPENDENCY
from src.enums.payment_processor import PaymentProcessorEnum
from src.models.account_settings import AccountSettings
from src.models.payment_processor import PaymentProcessor
from src.models.storefront import Storefront


class AccountSettingsService:
    def __init__(self, session: ASYNC_SESSION_DEPENDENCY):
        self._session = session

    async def get_payment_processor(self, subdomain: str) -> PaymentProcessorEnum:
        statement = (
            select(PaymentProcessor)
            .join(AccountSettings, PaymentProcessor.id == AccountSettings.payment_processor_id)
            .join(Storefront, AccountSettings.storefront_id == Storefront.id)
            .where(Storefront.subdomain == subdomain)
        )
        result = await self._session.exec(statement)
        payment_processor = result.one_or_none()
        return PaymentProcessorEnum(payment_processor.name)
