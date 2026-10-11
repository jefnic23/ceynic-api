from typing import Any

from fastapi import HTTPException, status
from pydantic import ValidationError
from sqlmodel import select

from src.database import ASYNC_SESSION_DEPENDENCY
from src.enums.payment_processor import PaymentProcessorEnum
from src.models.account_settings import AccountSettings
from src.models.storefront import Storefront
from src.schemas.payment_processor_selection import ConfiguredPaymentProcessors
from src.schemas.payment_processor_settings import PROCESSOR_CREDENTIALS, PaymentProcessorSettings
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

    async def get_configured_payment_processors(self, storefront_id: int) -> ConfiguredPaymentProcessors:
        statement = select(AccountSettings.payment_processor_settings).where(
            AccountSettings.storefront_id == storefront_id
        )
        result = await self._session.exec(statement)
        settings = result.one_or_none()
        if settings is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account settings not found")
        return ConfiguredPaymentProcessors(
            processors=[PaymentProcessorEnum(name) for name in settings.processors]
        )

    async def update_payment_processor_settings(
        self, storefront_id: int, processor: PaymentProcessorEnum, credentials: dict[str, Any]
    ) -> None:
        schema = PROCESSOR_CREDENTIALS.get(processor.value)
        if schema is None:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unsupported payment processor")
        try:
            validated = schema.model_validate(credentials).model_dump(mode="json", by_alias=False)
        except ValidationError as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=error.errors(include_input=False),
            ) from error

        statement = select(AccountSettings).where(
            AccountSettings.storefront_id == storefront_id
        ).with_for_update()
        result = await self._session.exec(statement)
        account_settings = result.one_or_none()
        if account_settings is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account settings not found")

        processors = {**account_settings.payment_processor_settings.processors, processor.value: validated}
        account_settings.payment_processor_settings = PaymentProcessorSettings(processors=processors)
        await self._session.commit()

    async def update_payment_processor(
        self, storefront_id: int, processor: PaymentProcessorEnum
    ) -> PaymentProcessorEnum:
        statement = select(AccountSettings).where(
            AccountSettings.storefront_id == storefront_id
        ).with_for_update()
        result = await self._session.exec(statement)
        account_settings = result.one_or_none()
        if account_settings is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account settings not found")

        if processor == PaymentProcessorEnum.NONE:
            account_settings.payment_processor = None
        else:
            if processor.value not in PROCESSOR_CREDENTIALS:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unsupported payment processor")
            if processor.value not in account_settings.payment_processor_settings.processors:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Processor credentials not configured")
            account_settings.payment_processor = processor.value

        await self._session.commit()
        return processor

    async def get_payment_processor(self, subdomain: str) -> PaymentProcessorEnum:
        statement = (
            select(AccountSettings.id, AccountSettings.payment_processor)
            .join(Storefront, AccountSettings.storefront_id == Storefront.id)
            .where(Storefront.subdomain == subdomain)
        )
        result = await self._session.exec(statement)
        row = result.one_or_none()
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account settings not found")
        _, name = row
        return PaymentProcessorEnum(name)

    async def get_paypal_client_id(self, subdomain: str) -> str:
        statement = (
            select(AccountSettings.payment_processor, AccountSettings.payment_processor_settings)
            .join(Storefront, AccountSettings.storefront_id == Storefront.id)
            .where(Storefront.subdomain == subdomain)
        )
        result = await self._session.exec(statement)
        row = result.one_or_none()
        if row is None or row[0] != PaymentProcessorEnum.PAYPAL.value:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PayPal is not enabled")

        credentials = row[1].processors.get(PaymentProcessorEnum.PAYPAL.value)
        if credentials is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PayPal is not configured")
        return credentials["client_id"]
