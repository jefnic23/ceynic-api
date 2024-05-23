from decimal import Decimal

from pydantic import BaseModel

from backend.src.models.enums.medium import Medium


class ProductBase(BaseModel):
    id: int
    title: str
    price: Decimal
    height: int
    width: int
    medium_id: Medium
    thumbnail: str


class ProductsOut(ProductBase):
    pass


class ProductOut(ProductBase):
    description: str | None
    slideshow: bool
    images: list[str]
