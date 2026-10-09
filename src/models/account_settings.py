from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.payment_processor import PaymentProcessor
    from src.models.storefront import Storefront


class AccountSettings(BaseModel, table=True):
    __tablename__ = "settings"

    id: int = Field(primary_key=True)

    storefront_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("storefronts.id", ondelete="CASCADE"), nullable=False
        )
    )
    storefront: "Storefront" = Relationship(back_populates="account_settings")

    payment_processor_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("payment_processors.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    payment_processor: "PaymentProcessor" = Relationship(back_populates="account_settings")
