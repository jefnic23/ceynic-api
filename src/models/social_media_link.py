from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.storefront import Storefront


class SocialMediaLink(SQLModel, table=True):
    __tablename__ = "social_media_links"

    id: int = Field(primary_key=True)
    name: str
    url: str
    
    storefront_id: int = Field(foreign_key='storefronts.id')
    storefront: "Storefront" = Relationship(back_populates="social_media_links")
