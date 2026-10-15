from decimal import Decimal

from src.schemas.base import BaseSchema


class ProductForOrder(BaseSchema):
    id: int
    title: str
    description: str | None = None
    price: Decimal
    quantity: int = 1
