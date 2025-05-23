from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Column, DateTime, Field, Relationship

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.order_product import OrderProduct
    from src.models.storefront import Storefront


class OrderBase(BaseModel):
    create_time: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    authorization_id: str
    capture_id: str
    status: str

    storefront_id: int = Field(foreign_key='storefronts.id')


class Order(OrderBase, table=True):
    __tablename__ = "orders"

    id: str = Field(primary_key=True)
    create_time: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    authorization_id: str
    capture_id: str
    status: str
    
    storefront: "Storefront" = Relationship(back_populates="orders")
    products: list["OrderProduct"] = Relationship(back_populates="order")


class OrdersOut(OrderBase):
    id: str
