from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.src.models.order import Order
    from backend.src.models.medium import Medium


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: int = Field(primary_key=True)
    title: str
    price: int
    height: int
    width: int
    description: str
    sold: bool
    slideshow: bool
    purchase_id: str | None
    thumbnail: str

    medium_id: int = Field(foreign_key="mediums.id")
    medium: "Medium" = Relationship(back_populates="products")

    order_id: str | None = Field(foreign_key="orders.id", unique=True)
    order: Optional["Order"] = Relationship(back_populates="products")
