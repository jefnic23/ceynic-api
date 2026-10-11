import inspect
from datetime import datetime, timezone
from functools import wraps
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import select

from src.database import ASYNC_SESSION_DEPENDENCY
from src.enums.payment_processor import PaymentProcessorEnum
from src.models.account_settings import AccountSettings
from src.models.order import Order, OrderOut
from src.models.order_product import OrderProduct
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

            # Only new checkouts use the storefront's current selection. All later
            # actions use the processor recorded when the external order was created.
            is_new_order = func.__name__ == "create_order"
            payment_processor, processor_name = await self._get_payment_processor(
                storefront_id,
                None if is_new_order else bound_args.arguments.get("order_id"),
            )

            # Inject payment_processor into kwargs
            bound_args.arguments["payment_processor"] = payment_processor
            if is_new_order:
                bound_args.arguments["processor_name"] = processor_name

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
        self, storefront_id: int, order_id: str, payment_processor: PaymentProcessorBase = None
    ) -> OrderDetails:
        return await payment_processor.get_order(storefront_id=storefront_id, order_id=order_id)

    @with_payment_processor
    async def create_order(
        self,
        storefront_id: int,
        products: list[ProductForOrder],
        payment_processor: PaymentProcessorBase = None,
        processor_name: str | None = None,
    ) -> CreateOrderOut:
        response = await payment_processor.create_order(storefront_id, products)
        self._session.add(
            Order(
                order_id=response.order_id,
                authorization_id=None,
                capture_id=None,
                status="CREATED",
                create_time=datetime.now(timezone.utc),
                storefront_id=storefront_id,
                payment_processor=processor_name,
            )
        )
        await self._session.commit()
        return response

    @with_payment_processor
    async def authorize_payment(
        self, storefront_id: int, order_id: str, product_ids: list[int], payment_processor: PaymentProcessorBase = None
    ) -> AuthorizePaymentResponse:
        existing = await self._session.exec(
            select(Order.authorization_id).where(Order.storefront_id == storefront_id, Order.order_id == order_id)
        )
        if existing.one_or_none() is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order already authorized")
        response = await payment_processor.authorize_payment(storefront_id=storefront_id, order_id=order_id)

        result = await self._session.exec(
            select(Order).where(Order.storefront_id == storefront_id, Order.order_id == order_id).with_for_update()
        )
        order = result.one_or_none()
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        if order.authorization_id is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order already authorized")

        order.authorization_id = response.authorization_id
        order.create_time = response.create_time
        order.status = "PENDING"  # todo: make this an enum
        for product_id in product_ids:
            self._session.add(OrderProduct(order_id=order.id, product_id=product_id))
        await self._session.commit()

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
        await self._session.commit()
        return response

    # region Private Methods

    async def _get_payment_processor(
        self, storefront_id: int, order_id: str | int | None = None
    ) -> tuple[PaymentProcessorBase, str]:
        if order_id is None:
            result = await self._session.exec(
                select(AccountSettings.payment_processor).where(
                    AccountSettings.storefront_id == storefront_id
                )
            )
            processor_name = result.one_or_none()
            if processor_name is None:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No payment processor selected")
        else:
            statement = select(Order).where(Order.storefront_id == storefront_id)
            if isinstance(order_id, int):
                statement = statement.where(Order.id == order_id)
            else:
                statement = statement.where(Order.order_id == order_id)
            result = await self._session.exec(statement)
            order = result.one_or_none()
            if order is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
            processor_name = order.payment_processor
            if processor_name is None:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order has no recorded payment processor")

        try:
            processor = PaymentProcessorEnum(processor_name)
        except ValueError as error:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payment processor unavailable") from error
        return self._payment_processor_factory.get_payment_processor(processor), processor_name

    # endregion
