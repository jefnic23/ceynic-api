from typing import Annotated
from fastapi import APIRouter, Depends, Response
from src.dependencies import SUBDOMAIN_DEPENDENCY
from src.enums.payment_processor import PaymentProcessorEnum
from src.services.account_settings_service import AccountSettingsService

router = APIRouter()


@router.get("/settings/paymentProcessor")
async def get_orders(
    subdomain: SUBDOMAIN_DEPENDENCY,
    account_settings_service: Annotated[AccountSettingsService, Depends()],
    response: Response
) -> PaymentProcessorEnum:
    payment_processor = await account_settings_service.get_payment_processor(subdomain)
    response.headers["cache-control"] = "max-age=3600"
    return payment_processor
