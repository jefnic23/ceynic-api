from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.product import Product
    from src.models.user import User


class Storefront(SQLModel, table=True):
    __tablename__ = "storefronts"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True)

    products: list[Product] = Relationship(back_populates="storefront")
    users: list[User] = Relationship(back_populates="storefront")
