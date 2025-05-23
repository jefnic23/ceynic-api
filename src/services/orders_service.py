import inspect

from functools import wraps
from typing import Annotated, TypeVar

from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database import get_async_session
from src.models.account_settings import AccountSettings
from src.enums.payment_processor import PaymentProcessorEnum
from src.models.payment_processor import PaymentProcessor
from src.schemas.create_order_out import CreateOrderOut
from src.schemas.paypal.authorize_payment_response import AuthorizePaymentResponse
from src.schemas.paypal.capture_payment_response import CapturePaymentResponse
from src.schemas.paypal.order_details import OrderDetails
from src.schemas.paypal.payments import Authorization
from src.schemas.product_for_order import ProductForOrder
from src.models.storefront import Storefront
from src.repositories.order_repository import OrderRepository
from src.services.base.payment_processor_base import PaymentProcessorBase
from src.services.factories.payment_processor_factory import PaymentProcessorFactory


class OrdersService:
    def __init__(
        self, 
        session: Annotated[AsyncSession, Depends(get_async_session)],
        order_repository: Annotated[OrderRepository, Depends()],
        payment_processor_factory: Annotated[PaymentProcessorFactory, Depends()] 
    ):
        self._session: AsyncSession = session
        self._order_repository: OrderRepository = order_repository
        self._payment_processor_factory: PaymentProcessorFactory = payment_processor_factory

    def with_payment_processor(func):
        @wraps(func)
        async def wrapper(self: "OrdersService", *args, **kwargs):
            # Get the function signature
            sig = inspect.signature(func)
            bound_args = sig.bind(self, *args, **kwargs)
            bound_args.apply_defaults()

            # Try to find storefront_id in args or kwargs
            storefront_id = bound_args.arguments.get('storefront_id')
            if storefront_id is None:
                raise ValueError(f"'storefront_id' must be provided to {func.__name__}")

            # Fetch payment processor
            payment_processor = await self._get_payment_processor(storefront_id)

            # Inject payment_processor into kwargs
            bound_args.arguments['payment_processor'] = payment_processor

            return await func(*bound_args.args, **bound_args.kwargs)
        return wrapper
    
    @with_payment_processor
    async def get_order(
        self, 
        storefront_id: int, 
        order_id: str, 
        payment_processor: PaymentProcessorBase = None
    ) -> OrderDetails:
        return await payment_processor.get_order(storefront_id=storefront_id, order_id=order_id)

    @with_payment_processor
    async def create_order(
        self, 
        storefront_id: int, 
        products: list[ProductForOrder], 
        payment_processor: PaymentProcessorBase = None
    ) -> CreateOrderOut:
        return await payment_processor.create_order(storefront_id, products)
    
    @with_payment_processor
    async def authorize_payment(
        self, 
        storefront_id: int, 
        order_id: str, 
        product_ids: list[int], 
        payment_processor: PaymentProcessorBase = None
    ) -> AuthorizePaymentResponse:
        return await payment_processor.authorize_payment(
            storefront_id=storefront_id,
            order_id=order_id, 
            product_ids=product_ids
        )
    
    @with_payment_processor
    async def reauthorize_payment(
        self, 
        storefront_id: int, 
        order_id: str,
        payment_processor: PaymentProcessorBase = None
    ) -> AuthorizePaymentResponse:
        return await payment_processor.reauthorize_payment(
            storefront_id=storefront_id,
            order_id=order_id
        )
    
    @with_payment_processor
    async def void_payment(
        self, 
        storefront_id: int, 
        order_id: str, 
        payment_processor: PaymentProcessorBase = None
    ) -> Authorization:
        return await payment_processor.void_payment(storefront_id=storefront_id, order_id=order_id)

    @with_payment_processor
    async def capture_payment(
        self, 
        storefront_id: int, 
        order_id: str, 
        payment_processor: PaymentProcessorBase = None
    ) -> CapturePaymentResponse:
        return await payment_processor.capture_payment(storefront_id, order_id=order_id)
    
    @with_payment_processor
    async def refund_payment(
        self, 
        storefront_id: int, 
        order_id: str, 
        payment_processor: PaymentProcessorBase = None
    ) -> CapturePaymentResponse:
        return await payment_processor.refund_payment(storefront_id, order_id=order_id)

    # region Private Methods

    async def _get_payment_processor(self, storefront_id: int) -> PaymentProcessorBase:
        statement = (
            select(PaymentProcessor)
            .join(AccountSettings, PaymentProcessor.id == AccountSettings.payment_processor_id)
            .join(Storefront, AccountSettings.storefront_id == Storefront.id)
            .where(Storefront.id == storefront_id)
        )
        result = await self._session.exec(statement)
        payment_processor = result.one_or_none()
        return self._payment_processor_factory.get_payment_processor(PaymentProcessorEnum(payment_processor.name))

    # endregion
