from fastapi import APIRouter, Response
from src.dependencies import ACCOUNT_SETTINGS_SERVICE_DEPENDENCY, SUBDOMAIN_DEPENDENCY
from src.enums.payment_processor import PaymentProcessorEnum

router = APIRouter()


@router.get("/settings/paymentProcessor")
async def get_orders(
    subdomain: SUBDOMAIN_DEPENDENCY,
    account_settings_service: ACCOUNT_SETTINGS_SERVICE_DEPENDENCY,
    response: Response
) -> PaymentProcessorEnum:
    payment_processor = await account_settings_service.get_payment_processor(subdomain)
    response.headers["cache-control"] = "max-age=3600"
    return payment_processor
