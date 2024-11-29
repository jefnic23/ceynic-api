from decimal import Decimal

from src.database import BaseSchema
from src.models.enums.medium import Medium


class ProductBase(BaseSchema):
    id: int
    title: str
    price: Decimal
    height: int
    width: int
    medium_id: Medium
    thumbnail: str


class ProductsOut(ProductBase):
    image_url: str


class ProductOut(ProductBase):
    description: str | None
    images: list[str]
