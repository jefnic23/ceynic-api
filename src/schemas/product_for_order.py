from decimal import Decimal

from src.schemas.base import BaseSchema


class ProductForOrder(BaseSchema):
    title: str
    description: str | None = None
    price: Decimal
    quantity: int = 1
