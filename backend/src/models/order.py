from datetime import datetime
from typing import TYPE_CHECKING
from decimal import Decimal

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

from backend.src.models.enums.order_status import OrderStatus

if TYPE_CHECKING:
    from backend.src.models.product import Product


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: str = Field(primary_key=True)
    status: OrderStatus
    create_time: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    address_1: str
    address_2: str
    city: str
    state: str
    postal_code: str
    country: str
    payer_first_name: str
    payer_last_name: str
    payer_email: str
    amount: Decimal

    products: list["Product"] = Relationship(back_populates="order")
