import inspect
from datetime import datetime
from functools import wraps
from typing import Annotated

from fastapi import Depends
from sqlmodel import select

from src.database import ASYNC_SESSION_DEPENDENCY
from src.enums.payment_processor import PaymentProcessorEnum
from src.models.account_settings import AccountSettings
from src.models.order import Order, OrderOut
from src.models.order_product import OrderProduct
from src.models.payment_processor import PaymentProcessor
from src.models.storefront import Storefront
from src.schemas.create_order_out import CreateOrderOut
from src.schemas.order_update import OrderUpdate
from src.schemas.paypal.authorize_payment_response import AuthorizePaymentResponse
from src.schemas.paypal.capture_payment_response import CapturePaymentResponse
from src.schemas.paypal.order_details import OrderDetails
from src.schemas.paypal.payments import Authorization
from src.schemas.product_for_order import ProductForOrder
from src.services.base.payment_processor_base import PaymentProcessorBase
from src.services.factories.payment_processor_factory import PaymentProcessorFactory


class OrdersService:
    def __init__(
        self,
        session: ASYNC_SESSION_DEPENDENCY,
        payment_processor_factory: Annotated[PaymentProcessorFactory, Depends()],
    ):
        self._session = session
        self._payment_processor_factory = payment_processor_factory

    def with_payment_processor(func):
        @wraps(func)
        async def wrapper(self: "OrdersService", *args, **kwargs):
            # Get the function signature
            sig = inspect.signature(func)
            bound_args = sig.bind(self, *args, **kwargs)
            bound_args.apply_defaults()

            # Try to find storefront_id in args or kwargs
            storefront_id = bound_args.arguments.get("storefront_id")
            if storefront_id is None:
                raise ValueError(f"'storefront_id' must be provided to {func.__name__}")

            # Fetch payment processor
            payment_processor = await self._get_payment_processor(storefront_id)

            # Inject payment_processor into kwargs
            bound_args.arguments["payment_processor"] = payment_processor

            return await func(*bound_args.args, **bound_args.kwargs)

        return wrapper

    async def get_all(self, storefront_id: int) -> list[OrderOut]:
        statement = select(Order).where(Order.storefront_id == storefront_id).order_by(Order.create_time.desc())
        results = await self._session.exec(statement=statement)
        return results.all()

    async def get(self, storefront_id: int, order_id: int) -> Order | None:
        statement = select(Order).where(Order.storefront_id == storefront_id).where(Order.id == order_id)
        results = await self._session.exec(statement=statement)
        return results.one_or_none()

    async def get_authorization_id(self, storefront_id: int, order_id: int) -> str | None:
        statement = (
            select(Order.authorization_id).where(Order.storefront_id == storefront_id).where(Order.id == order_id)
        )
        results = await self._session.exec(statement=statement)
        return results.one_or_none()

    async def get_capture_id(self, storefront_id: int, order_id: int) -> str | None:
        statement = select(Order.capture_id).where(Order.storefront_id == storefront_id).where(Order.id == order_id)
        results = await self._session.exec(statement=statement)
        return results.one_or_none()

    async def add(
        self,
        order_id: str,
        create_time: datetime,
        storefront_id: int,
        authorization_id: str,
        status: str,
        product_ids: list[int],
    ) -> Order:
        order_products = [OrderProduct(product_id=product_id) for product_id in product_ids]
        order = Order(
            order_id=order_id,
            authorization_id=authorization_id,
            status=status,
            create_time=create_time,
            storefront_id=storefront_id,
            products=order_products,
        )
        self._session.add(order)
        return order

    async def update(self, storefront_id: int, order_id: int, updates: OrderUpdate) -> Order | None:
        order = await self.get(storefront_id=storefront_id, order_id=order_id)
        if not order:
            return

        update_data = updates.model_dump(exclude_unset=True)
        if not update_data:
            return

        for key, value in update_data.items():
            setattr(order, key, value)

        return order

    @with_payment_processor
    async def get_order(
        self, storefront_id: int, order_id: int, payment_processor: PaymentProcessorBase = None
    ) -> OrderDetails:
        return await payment_processor.get_order(storefront_id=storefront_id, order_id=order_id)

    @with_payment_processor
    async def create_order(
        self, storefront_id: int, products: list[ProductForOrder], payment_processor: PaymentProcessorBase = None
    ) -> CreateOrderOut:
        return await payment_processor.create_order(storefront_id, products)

    @with_payment_processor
    async def authorize_payment(
        self, storefront_id: int, order_id: int, product_ids: list[int], payment_processor: PaymentProcessorBase = None
    ) -> AuthorizePaymentResponse:
        response = await payment_processor.authorize_payment(storefront_id=storefront_id, order_id=order_id)

        order = await self.add(
            order_id=order_id,
            create_time=response.create_time,
            storefront_id=storefront_id,
            authorization_id=response.authorization_id,
            status="PENDING",  # todo: make this an enum
            product_ids=product_ids,
        )
        await self._session.commit()
        await self._session.refresh(order)

    @with_payment_processor
    async def reauthorize_payment(
        self, storefront_id: int, order_id: int, payment_processor: PaymentProcessorBase = None
    ) -> AuthorizePaymentResponse:
        authorization_id = await self.get_authorization_id(storefront_id=storefront_id, order_id=order_id)

        response = await payment_processor.reauthorize_payment(
            storefront_id=storefront_id, authorization_id=authorization_id
        )

        order = await self.update(
            storefront_id=storefront_id,
            order_id=order_id,
            updates=OrderUpdate(status="PENDING", authorization_id=response.id),
        )
        await self._session.commit()
        await self._session.refresh(order)

        return response

    @with_payment_processor
    async def void_payment(
        self, storefront_id: int, order_id: int, payment_processor: PaymentProcessorBase = None
    ) -> Authorization:
        authorization_id = await self.get_authorization_id(storefront_id=storefront_id, order_id=order_id)

        response = await payment_processor.void_payment(storefront_id=storefront_id, authorization_id=authorization_id)

        order = await self.update(
            storefront_id=storefront_id, order_id=order_id, updates=OrderUpdate(status=response.status)
        )
        await self._session.commit()
        await self._session.refresh(order)

        return response

    @with_payment_processor
    async def capture_payment(
        self, storefront_id: int, order_id: int, payment_processor: PaymentProcessorBase = None
    ) -> CapturePaymentResponse:
        authorization_id = await self.get_authorization_id(storefront_id=storefront_id, order_id=order_id)

        response = await payment_processor.capture_payment(storefront_id, authorization_id=authorization_id)

        order = await self.update(
            storefront_id=storefront_id,
            order_id=order_id,
            updates=OrderUpdate(capture_id=response.id, status="COMPLETED"),
        )
        await self._session.commit()
        await self._session.refresh(order)

        return response

    @with_payment_processor
    async def refund_payment(
        self, storefront_id: int, order_id: int, payment_processor: PaymentProcessorBase = None
    ) -> CapturePaymentResponse:
        capture_id = await self.get_capture_id(storefront_id=storefront_id, order_id=order_id)

        response = await payment_processor.refund_payment(storefront_id, capture_id=capture_id)

        await self.update(storefront_id=storefront_id, order_id=order_id, updates=OrderUpdate(status="REFUNDED"))

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
