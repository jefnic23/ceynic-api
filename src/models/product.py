from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.medium import Medium
    from src.models.order import Order
    from src.models.storefront import Storefront


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: int = Field(primary_key=True)
    title: str
    price: Decimal
    height: int
    width: int
    description: str | None
    sold: bool
    thumbnail: str
    date_added: datetime

    medium_id: int = Field(foreign_key="mediums.id")
    medium: "Medium" = Relationship(back_populates="products")

    order_id: str | None = Field(foreign_key="orders.id", unique=True)
    order: Optional["Order"] = Relationship(back_populates="products")

    storefront_id: int = Field(foreign_key="storefronts.id")
    storefront: "Storefront" = Relationship(back_populates="products")
