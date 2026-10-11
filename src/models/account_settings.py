from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, text
from sqlmodel import Field, Relationship

from src.models.base import BaseModel
from src.models.payment_processor_settings_type import PaymentProcessorSettingsType
from src.models.payment_processor_type import PaymentProcessorType
from src.models.site_settings_type import SiteSettingsType
from src.schemas.payment_processor_settings import PaymentProcessorSettings
from src.schemas.site_settings import SiteSettings

if TYPE_CHECKING:
    from src.models.storefront import Storefront


class AccountSettings(BaseModel, table=True):
    __tablename__ = "settings"

    id: int = Field(primary_key=True)
    site_settings: SiteSettings = Field(
        default_factory=SiteSettings,
        sa_column=Column(SiteSettingsType(), nullable=False, server_default=text("'{}'::jsonb")),
    )
    payment_processor_settings: PaymentProcessorSettings = Field(
        default_factory=PaymentProcessorSettings,
        sa_column=Column(
            PaymentProcessorSettingsType(),
            nullable=False,
            server_default=text("'{\"processors\": {}}'::jsonb"),
        ),
    )

    storefront_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("storefronts.id", ondelete="CASCADE"), nullable=False
        )
    )
    storefront: "Storefront" = Relationship(back_populates="account_settings")

    payment_processor: str | None = Field(
        default=None,
        sa_column=Column(PaymentProcessorType, nullable=True),
    )
