from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.refresh_token import RefreshToken
    from src.models.storefront import Storefront


class User(BaseModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)
    email: str = Field(unique=True)
    password: str

    storefront_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("storefronts.id", ondelete="CASCADE"), nullable=False
        )
    )
    storefront: "Storefront" = Relationship(back_populates="users")

    refresh_token: Optional["RefreshToken"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False}
    )
