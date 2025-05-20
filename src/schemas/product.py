from decimal import Decimal

from src.database import BaseSchema


class ProductBase(BaseSchema):
    id: int
    title: str
    price: Decimal
    height: int
    width: int
    medium_id: int
    thumbnail: str
    enabled: bool


class ProductsOut(ProductBase):
    image_url: str


class ProductOut(ProductBase):
    description: str | None
    images: list[str]
