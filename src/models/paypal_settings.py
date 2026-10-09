from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlmodel import Field, Relationship

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.storefront import Storefront


class PayPalSettings(BaseModel, table=True):
    __tablename__ = "paypal_settings"
    __table_args__ = (
        UniqueConstraint("storefront_id", name="uq_paypal_settings_storefront_id"),
    )

    id: int = Field(primary_key=True)
    client_id: str
    client_secret: str

    storefront_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("storefronts.id", ondelete="CASCADE"), nullable=False
        )
    )
    storefront: "Storefront" = Relationship(back_populates="paypal_settings")
