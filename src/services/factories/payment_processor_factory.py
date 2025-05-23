from typing import Annotated

from fastapi import Depends
from src.database import get_async_session
from src.enums.payment_processor import PaymentProcessorEnum
from src.repositories.order_repository import OrderRepository
from src.services.base.payment_processor_base import PaymentProcessorBase
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Settings, get_settings
from src.http_client import HttpClient
from src.services.base.payment_processor_base import PaymentProcessorBase
from src.services.paypal_service import PayPalService

class PaymentProcessorFactory:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_async_session)], 
        settings: Annotated[Settings, Depends(get_settings)], 
        http_client: Annotated[HttpClient, Depends()],
        order_repository: Annotated[OrderRepository, Depends()]
    ):
        self._session: AsyncSession = session
        self._settings: Settings = settings
        self._http_client: HttpClient = http_client
        self._order_repository: OrderRepository = order_repository

    def get_payment_processor(self, payment_processor: PaymentProcessorEnum) -> PaymentProcessorBase:
        if payment_processor == PaymentProcessorEnum.PAYPAL:
            return PayPalService(
                session=self._session, 
                settings=self._settings, 
                http_client=self._http_client,
                order_repository=self._order_repository
            )
        # elif merchant.payment_provider == "stripe":
        #     return StripeProcessor()
        # elif merchant.payment_provider == "amazon_pay":
        #     return StripeProcessor()
        else:
            raise ValueError(f"Unknown payment provider: {PaymentProcessorEnum.value}")
