from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from backend.src.models.enums.medium import Medium

if TYPE_CHECKING:
    from backend.src.models.order import Order


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: int = Field(primary_key=True)
    title: str
    price: int
    # medium: Medium
    medium: str
    height: int
    width: int
    description: str
    sold: bool
    slideshow: bool
    purchase_id: str | None
    # image_url: str

    # order_id: str | None = Field(foreign_key="orders.id", unique=True)
    # order: Optional["Order"] = Relationship(back_populates="product")
