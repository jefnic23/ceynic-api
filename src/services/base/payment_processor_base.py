from abc import ABC, abstractmethod

from src.schemas.create_order_out import CreateOrderOut
from src.schemas.paypal.order_details import OrderDetails
from src.schemas.product_for_order import ProductForOrder


class PaymentProcessorBase(ABC):
    @abstractmethod
    async def get_order(self, storefront_id: int, order_id: str) -> OrderDetails:
        pass

    @abstractmethod
    async def create_order(self, storefront_id: int, products: list[ProductForOrder], **kwargs) -> CreateOrderOut:
        pass

    @abstractmethod
    async def authorize_payment(self, storefront_id: int, order_id: str, product_ids: list[int], **kwargs):
        pass

    @abstractmethod
    async def reauthorize_payment(self, storefront_id: int, order_id: str, **kwargs):
        pass

    @abstractmethod
    async def void_payment(self, storefront_id: int, order_id: str, **kwargs):
        pass

    @abstractmethod
    async def capture_payment(self, storefront_id: int, order_id: str, **kwargs) -> dict:
        pass

    @abstractmethod
    async def refund_payment(self, storefront_id: int, order_id: str, **kwargs) -> dict:
        pass
