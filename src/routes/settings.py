from typing import Annotated

from fastapi import APIRouter, Depends, Response

from src.dependencies import CURRENT_USER_DEPENDENCY, SUBDOMAIN_DEPENDENCY
from src.enums.payment_processor import PaymentProcessorEnum
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
async def get_orders(
    subdomain: SUBDOMAIN_DEPENDENCY,
    account_settings_service: Annotated[AccountSettingsService, Depends()],
    response: Response,
) -> PaymentProcessorEnum:
    payment_processor = await account_settings_service.get_payment_processor(subdomain)
    response.headers["cache-control"] = "max-age=3600"
    return payment_processor
