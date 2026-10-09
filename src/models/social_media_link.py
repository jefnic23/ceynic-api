from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship

from src.decorators import frontend
from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.storefront import Storefront


class SocialMediaLinkBase(BaseModel):
    name: str
    url: str

    storefront_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("storefronts.id", ondelete="CASCADE"), nullable=False
        )
    )


class SocialMediaLink(SocialMediaLinkBase, table=True):
    __tablename__ = "social_media_links"

    id: int = Field(primary_key=True)
    name: str
    url: str
    
    storefront: "Storefront" = Relationship(back_populates="social_media_links")


@frontend
class SocialMediaLinkOut(SocialMediaLinkBase):
    id: int
    name: str
    url: str
