from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.account_settings import AccountSettings
    from src.models.storefront import Storefront


class PayPalSettings(SQLModel, table=True):
    __tablename__ = "paypal_settings"

    id: str = Field(primary_key=True)
    client_id: str
    client_secret: str

    storefront_id: int = Field(foreign_key='storefronts.id')
    storefront: "Storefront" = Relationship(back_populates="paypal_settings")
