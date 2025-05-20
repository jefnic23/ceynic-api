from decimal import Decimal
from src.database import BaseSchema


class ProductForOrder(BaseSchema):
    title: str
    price: Decimal
