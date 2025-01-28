from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from src.models.content import Content

if TYPE_CHECKING:
    from src.models.product import Product
    from src.models.user import User


class Storefront(SQLModel, table=True):
    __tablename__ = "storefronts"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    city: str
    state: str = Field(nullable=False)

    content: Optional["Content"] = Relationship(
        back_populates="storefront", sa_relationship_kwargs={"uselist": False}
    )

    products: list["Product"] = Relationship(back_populates="storefront")
    users: list["User"] = Relationship(back_populates="storefront")
