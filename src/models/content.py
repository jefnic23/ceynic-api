from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.storefront import Storefront


class ContentBase(BaseModel):
    about: str


class Content(ContentBase, table=True):
    __tablename__ = "contents"
    __table_args__ = (UniqueConstraint("storefront_id", name="uq_contents_storefront_id"),)

    id: int = Field(primary_key=True)

    storefront_id: int = Field(foreign_key="storefronts.id")
    storefront: "Storefront" = Relationship(back_populates="content")
