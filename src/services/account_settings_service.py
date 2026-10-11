from fastapi import HTTPException, status
from sqlmodel import select

from src.database import ASYNC_SESSION_DEPENDENCY
from src.enums.payment_processor import PaymentProcessorEnum
from src.models.account_settings import AccountSettings
from src.models.payment_processor import PaymentProcessor
from src.models.storefront import Storefront
from src.schemas.site_settings import SiteSettings


class AccountSettingsService:
    def __init__(self, session: ASYNC_SESSION_DEPENDENCY):
        self._session = session

    async def get_site_settings(self, subdomain: str) -> SiteSettings:
        statement = (
            select(AccountSettings.site_settings)
            .join(Storefront, AccountSettings.storefront_id == Storefront.id)
            .where(Storefront.subdomain == subdomain)
        )
        result = await self._session.exec(statement)
        site_settings = result.one_or_none()
        if site_settings is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site settings not found")
        return site_settings

    async def update_site_settings(self, storefront_id: int, site_settings: SiteSettings) -> SiteSettings:
        statement = select(AccountSettings).where(AccountSettings.storefront_id == storefront_id)
        result = await self._session.exec(statement)
        account_settings = result.one_or_none()
        if account_settings is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site settings not found")

        account_settings.site_settings = site_settings
        await self._session.commit()
        return site_settings

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
