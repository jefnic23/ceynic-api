from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Annotated

from fastapi import File, Form, UploadFile
from sqlalchemy import Column, DateTime, func
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
    description: str | None = None
    enabled: bool
    date_added: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
    )

    medium_id: int = Field(foreign_key="mediums.id")
    storefront_id: int = Field(foreign_key="storefronts.id")


class Product(ProductBase, table=True):
    __tablename__ = "products"

    id: int = Field(primary_key=True)

    medium: "Medium" = Relationship(back_populates="products")
    storefront: "Storefront" = Relationship(back_populates="products")

    images: list["ProductImage"] = Relationship(
        back_populates="product", sa_relationship_kwargs={"order_by": "ProductImage.position"}
    )
    orders: list["OrderProduct"] = Relationship(back_populates="product")


@frontend
class ProductOut(ProductBase):
    id: int
    images: list[ProductImageOut] = None
    medium: MediumOut | None = None


@frontend
class ProductForCreate(BaseModel):
    title: Annotated[str, Form()]
    description: Annotated[str | None, Form()] = None
    price: Annotated[Decimal, Form()]
    medium_id: Annotated[int, Form()]
    height: Annotated[int, Form()]
    width: Annotated[int, Form()]
    enabled: Annotated[bool, Form()]
    images: Annotated[list[UploadFile], File(min_length=1)]


@frontend
class ProductForUpdate(BaseModel):
    id: Annotated[int, Form()]
    title: Annotated[str, Form()]
    description: Annotated[str | None, Form()] = None
    price: Annotated[Decimal, Form()]
    medium_id: Annotated[int, Form()]
    height: Annotated[int, Form()]
    width: Annotated[int, Form()]
    enabled: Annotated[bool, Form()]
    images: Annotated[list[UploadFile] | None, File()] = None
