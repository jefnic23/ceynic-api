from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlmodel import Field, Relationship

from src.decorators import frontend
from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.order_product import OrderProduct
    from src.models.storefront import Storefront


class OrderBase(BaseModel):
    order_id: str
    authorization_id: str | None
    capture_id: str | None
    status: str
    create_time: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )

    storefront_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("storefronts.id", ondelete="CASCADE"), nullable=False
        )
    )


class Order(OrderBase, table=True):
    __tablename__ = "orders"

    id: int = Field(primary_key=True) 
    
    storefront: "Storefront" = Relationship(back_populates="orders")
    products: list["OrderProduct"] = Relationship(back_populates="order")


@frontend
class OrderOut(OrderBase):
    id: int
