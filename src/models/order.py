from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.order_product import OrderProduct


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: str = Field(primary_key=True)

    products: list["OrderProduct"] = Relationship(back_populates="order")
