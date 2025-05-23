from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.storefront import Storefront


class SocialMediaLinkBase(BaseModel):
    name: str
    url: str

    storefront_id: int = Field(foreign_key='storefronts.id')


class SocialMediaLink(SocialMediaLinkBase, table=True):
    __tablename__ = "social_media_links"

    id: int = Field(primary_key=True)
    name: str
    url: str
    
    storefront: "Storefront" = Relationship(back_populates="social_media_links")


class SocialMediaLinkOut(SocialMediaLinkBase):
    id: int
    name: str
    url: str
