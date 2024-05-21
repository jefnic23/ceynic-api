from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

from backend.src.models.enums.order_status import OrderStatus

if TYPE_CHECKING:
    from backend.src.models.product import Product


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: str = Field(primary_key=True)
    status: OrderStatus
    create_time: datetime = Field(sa_column=Column(DateTime(timezone=True)))

    product: Optional["Product"] = Relationship(
        back_populates="order", sa_relationship_kwargs={"uselist": False}
    )
