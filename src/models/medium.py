from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.product import Product


class MediumBase(BaseModel):
    name: str


class Medium(MediumBase, table=True):
    __tablename__ = "mediums"

    id: int = Field(primary_key=True)

    products: list["Product"] = Relationship(back_populates="medium")


class MediumOut(MediumBase):
    id: int
