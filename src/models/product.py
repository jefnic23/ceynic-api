from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from fastapi import Form, UploadFile
from sqlmodel import Field, Relationship

from src.decorators import frontend
from src.models.base import BaseModel
from src.models.medium import MediumOut
from src.models.product_image import ProductImageOut

if TYPE_CHECKING:
    from src.models.medium import Medium
    from src.models.order_product import OrderProduct
    from src.models.product_image import ProductImage
    from src.models.storefront import Storefront


class ProductBase(BaseModel):
    title: str
    price: Decimal
    height: int
    width: int
    description: str | None
    enabled: bool
    thumbnail: str # todo: deprecate
    date_added: datetime
    # quantity: int

    medium_id: int = Field(foreign_key="mediums.id")
    storefront_id: int = Field(foreign_key="storefronts.id")


class Product(ProductBase, table=True):
    __tablename__ = "products"

    id: int = Field(primary_key=True)

    medium: "Medium" = Relationship(back_populates="products")
    storefront: "Storefront" = Relationship(back_populates="products")
    
    images: list["ProductImage"] = Relationship(back_populates="product")
    orders: list["OrderProduct"] = Relationship(back_populates="product")


@frontend  
class ProductOut(ProductBase):
    id: int
    images: list[ProductImageOut] = []
    medium: MediumOut | None = None


# todo: should this be a frontend model?
class ProductIn(BaseModel):
    id: int
    title: str
    description: str | None
    price: Decimal
    medium_id: int
    height: int
    width: int
    enabled: bool
    images: list[UploadFile] = []
