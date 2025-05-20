from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.account_settings import AccountSettings
from src.enums.payment_processor import PaymentProcessorEnum
from src.models.payment_processor import PaymentProcessor
from src.models.storefront import Storefront

class AccountSettingsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_payment_processor(self, subdomain: str) -> PaymentProcessorEnum:
        statement = (
            select(PaymentProcessor)
            .join(AccountSettings, PaymentProcessor.id == AccountSettings.payment_processor_id)
            .join(Storefront, AccountSettings.storefront_id == Storefront.id)
            .where(Storefront.subdomain == subdomain)
        )
        result = await self.session.exec(statement)
        payment_processor = result.one_or_none()
        return PaymentProcessorEnum(payment_processor.name)
