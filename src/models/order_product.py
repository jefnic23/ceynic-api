from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.order import Order
    from src.models.product import Product


class OrderProduct(SQLModel, table=True):
    __tablename__ = "order_products"

    id: int = Field(primary_key=True)

    order_id: str = Field(foreign_key="orders.id")
    order: "Order" = Relationship(back_populates="products")

    product_id: int = Field(foreign_key="products.id")
    product: "Product" = Relationship(back_populates="orders")
