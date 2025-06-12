from src.database import BaseSchema
from src.schemas.paypal.base import Tax, UnitAmount


class DiscountPercent(BaseSchema):
    percent: str


class DiscountAmount(BaseSchema):
    amount: UnitAmount


class Item(BaseSchema):
    name: str
    quantity: str
    unit_amount: UnitAmount | None = None
    tax: Tax | None = None
    discount: DiscountPercent | DiscountAmount | None = None
    description: str | None = None
    unit_of_measure: str | None = None
