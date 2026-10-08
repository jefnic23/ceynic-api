from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.account_settings import AccountSettings


class PaymentProcessor(SQLModel, table=True):
    __tablename__ = "payment_processors"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True)

    account_settings: list["AccountSettings"] = Relationship(back_populates="payment_processor")
