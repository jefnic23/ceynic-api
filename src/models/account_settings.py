from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, text
from sqlmodel import Field, Relationship

from src.models.base import BaseModel
from src.models.site_settings_type import SiteSettingsType
from src.schemas.site_settings import SiteSettings

if TYPE_CHECKING:
    from src.models.payment_processor import PaymentProcessor
    from src.models.storefront import Storefront


class AccountSettings(BaseModel, table=True):
    __tablename__ = "settings"

    id: int = Field(primary_key=True)
    site_settings: SiteSettings = Field(
        default_factory=SiteSettings,
        sa_column=Column(SiteSettingsType(), nullable=False, server_default=text("'{}'::jsonb")),
    )

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
