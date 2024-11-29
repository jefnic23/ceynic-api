from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.product import Product


class Medium(SQLModel, table=True):
    __tablename__ = "mediums"

    id: int = Field(primary_key=True)
    name: str

    products: list["Product"] = Relationship(back_populates="medium")
