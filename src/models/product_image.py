from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship
from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.product import Product


class ProductImageBase(BaseModel):
    public_id: str
    position: int
    width: int
    height: int

    product_id: int = Field(foreign_key="products.id")


class ProductImage(ProductImageBase, table=True):
    __tablename__ = "product_images"

    id: int = Field(primary_key=True)

    product: "Product" = Relationship(back_populates="images")


class ProductImageOut(ProductImageBase):
    id: int
