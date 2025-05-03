from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from src.models.account_settings import AccountSettings
    from src.models.content import Content
    from src.models.order import Order
    from src.models.paypal_settings import PayPalSettings
    from src.models.product import Product
    from src.models.user import User


class Storefront(SQLModel, table=True):
    __tablename__ = "storefronts"

    id: int = Field(primary_key=True)
    name: str
    city: str
    state: str = Field(nullable=False)
    subdomain: str = Field(unique=True)

    content: Optional["Content"] = Relationship(
        back_populates="storefront", sa_relationship_kwargs={"uselist": False}
    )
    paypal_settings: Optional["PayPalSettings"] = Relationship(
        back_populates="storefront", sa_relationship_kwargs={"uselist": False}
    )

    account_settings: list["AccountSettings"] = Relationship(back_populates="storefront")
    orders: list["Order"] = Relationship(back_populates="storefront") 
    products: list["Product"] = Relationship(back_populates="storefront")
    users: list["User"] = Relationship(back_populates="storefront")
