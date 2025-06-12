from src.schemas.base import BaseSchema
from src.schemas.paypal.base import Amount, Payee
from src.schemas.paypal.item import Item
from src.schemas.paypal.payments import Payments
from src.schemas.paypal.shipping import Shipping


class PurchaseUnit(BaseSchema):
    reference_id: str | None = None
    payee: Payee | None = None
    description: str | None = None
    shipping: Shipping | None = None
    payments: Payments | None = None
    amount: Amount | None = None
    items: list[Item] | None = None
