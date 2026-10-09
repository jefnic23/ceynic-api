from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.order import Order
    from src.models.product import Product


class OrderProductBase(BaseModel):
    order_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
        )
    )
    product_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
        )
    )


class OrderProduct(OrderProductBase, table=True):
    __tablename__ = "order_products"

    id: int = Field(primary_key=True)

    order: "Order" = Relationship(back_populates="products")
    product: "Product" = Relationship(back_populates="orders")
