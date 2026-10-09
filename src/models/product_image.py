from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship, UniqueConstraint

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.product import Product


class ProductImageBase(BaseModel):
    url: str
    position: int
    width: int
    height: int

    product_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
        )
    )


class ProductImage(ProductImageBase, table=True):
    __tablename__ = "product_images"
    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "position",
            name="uq_product_images_product_id_position",
            deferrable=True,
            initially="DEFERRED",
        ),
    )

    id: int = Field(primary_key=True)

    product: "Product" = Relationship(back_populates="images")


class ProductImageOut(ProductImageBase):
    id: int
