from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.src.models.product import Product


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: str = Field(primary_key=True)

    products: list["Product"] = Relationship(back_populates="order")
