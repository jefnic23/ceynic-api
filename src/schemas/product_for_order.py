from decimal import Decimal
from src.database import BaseSchema


class ProductForOrder(BaseSchema):
    title: str
    description: str | None = None
    price: Decimal
