from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.payment_processor import PaymentProcessor
    from src.models.storefront import Storefront


class AccountSettings(SQLModel, table=True):
    __tablename__ = "settings"

    id: str = Field(primary_key=True)

    storefront_id: int = Field(foreign_key='storefronts.id')
    storefront: "Storefront" = Relationship(back_populates="account_settings")

    payment_processor_id: int = Field(foreign_key='payment_processors.id')
    payment_processor: "PaymentProcessor" = Relationship(back_populates="account_settings")
