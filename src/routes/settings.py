from typing import Annotated, Any

from fastapi import APIRouter, Depends, Response, status

from src.dependencies import CURRENT_USER_DEPENDENCY, SUBDOMAIN_DEPENDENCY
from src.enums.payment_processor import PaymentProcessorEnum
from src.schemas.payment_processor_selection import ConfiguredPaymentProcessors, PaymentProcessorSelection
from src.schemas.site_settings import SiteSettings
from src.services.account_settings_service import AccountSettingsService

router = APIRouter()


@router.get("/settings/siteSettings")
async def get_site_settings(
    subdomain: SUBDOMAIN_DEPENDENCY,
    account_settings_service: Annotated[AccountSettingsService, Depends()],
) -> SiteSettings:
    return await account_settings_service.get_site_settings(subdomain)


@router.put("/settings/siteSettings")
async def update_site_settings(
    current_user: CURRENT_USER_DEPENDENCY,
    account_settings_service: Annotated[AccountSettingsService, Depends()],
    site_settings: SiteSettings,
) -> SiteSettings:
    return await account_settings_service.update_site_settings(current_user.storefront_id, site_settings)


@router.get("/settings/paymentProcessor")
async def get_payment_processor(
    subdomain: SUBDOMAIN_DEPENDENCY,
    account_settings_service: Annotated[AccountSettingsService, Depends()],
    response: Response,
) -> PaymentProcessorEnum:
    payment_processor = await account_settings_service.get_payment_processor(subdomain)
    response.headers["cache-control"] = "no-store"
    return payment_processor


@router.get("/settings/paypalClientId")
async def get_paypal_client_id(
    subdomain: SUBDOMAIN_DEPENDENCY,
    account_settings_service: Annotated[AccountSettingsService, Depends()],
    response: Response,
) -> dict[str, str]:
    client_id = await account_settings_service.get_paypal_client_id(subdomain)
    response.headers["cache-control"] = "no-store"
    return {"clientId": client_id}


@router.put("/settings/paymentProcessor")
async def update_payment_processor(
    current_user: CURRENT_USER_DEPENDENCY,
    account_settings_service: Annotated[AccountSettingsService, Depends()],
    selection: PaymentProcessorSelection,
) -> PaymentProcessorEnum:
    return await account_settings_service.update_payment_processor(
        current_user.storefront_id, selection.processor
    )


@router.get("/settings/paymentProcessorSettings")
async def get_configured_payment_processors(
    current_user: CURRENT_USER_DEPENDENCY,
    account_settings_service: Annotated[AccountSettingsService, Depends()],
    response: Response,
) -> ConfiguredPaymentProcessors:
    response.headers["cache-control"] = "no-store"
    return await account_settings_service.get_configured_payment_processors(current_user.storefront_id)


@router.put("/settings/paymentProcessorSettings/{processor}", status_code=status.HTTP_204_NO_CONTENT)
async def update_payment_processor_settings(
    processor: PaymentProcessorEnum,
    current_user: CURRENT_USER_DEPENDENCY,
    account_settings_service: Annotated[AccountSettingsService, Depends()],
    credentials: dict[str, Any],
) -> None:
    await account_settings_service.update_payment_processor_settings(
        current_user.storefront_id, processor, credentials
    )
