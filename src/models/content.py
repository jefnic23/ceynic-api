from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.storefront import Storefront


class Content(SQLModel, table=True):
    __tablename__ = "contents"

    id: int = Field(primary_key=True)
    about: str

    storefront_id: int = Field(foreign_key='storefronts.id')
    storefront: "Storefront" = Relationship(back_populates="content")
