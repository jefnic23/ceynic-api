from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from src.models.base import BaseModel
from src.models.medium import MediumOut

if TYPE_CHECKING:
    from src.models.medium import Medium
    from src.models.order_product import OrderProduct
    from src.models.storefront import Storefront


class ProductBase(BaseModel):
    title: str
    price: Decimal
    height: int
    width: int
    description: str | None
    enabled: bool
    thumbnail: str
    date_added: datetime

    medium_id: int = Field(foreign_key="mediums.id")
    storefront_id: int = Field(foreign_key="storefronts.id")

    @property
    def formatted_title(self) -> str:
        return self.title.replace(' ', '_')


class Product(ProductBase, table=True):
    __tablename__ = "products"

    id: int = Field(primary_key=True)

    medium: "Medium" = Relationship(back_populates="products")
    storefront: "Storefront" = Relationship(back_populates="products")
    orders: list["OrderProduct"] = Relationship(back_populates="product")

    
class ProductsOut(ProductBase):
    id: int
    image_url: str | None = None # todo: maybe the full thumbnail url should be stored in the db?
    medium: MediumOut | None = None

    @classmethod
    def from_product(cls, product: ProductBase, bucket_name: str) -> "ProductsOut":
        return cls(
            **product.model_dump(),
            medium=MediumOut.model_validate(product.medium) if product.medium else None,
            image_url=f"https://{bucket_name}.s3.amazonaws.com/public/{product.formatted_title}/{product.thumbnail}",
        )


class ProductOut(ProductBase):
    id: int
    images: list[str] = []
    medium: MediumOut | None = None

    @classmethod
    def from_product(cls, product: ProductBase, images: list[str]) -> "ProductOut":
        return cls(
            **product.model_dump(),
            medium=MediumOut.model_validate(product.medium) if product.medium else None,
            images=images,
        )
