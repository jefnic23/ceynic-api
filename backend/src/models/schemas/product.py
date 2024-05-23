from decimal import Decimal

from pydantic import BaseModel


class ProductBase(BaseModel):
    id: int
    title: str
    price: Decimal
    height: int
    width: int
    thumbnail: str


class ProductsOut(ProductBase):
    pass


class ProductOut(ProductBase):
    description: str | None
    slideshow: bool
    images: list[str]
