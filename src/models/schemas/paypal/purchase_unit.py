from src.database import BaseSchema
from src.models.schemas.paypal.base import Amount, Payee
from src.models.schemas.paypal.payments import Payments
from src.models.schemas.paypal.shipping import Shipping


class PurchaseUnit(BaseSchema):
    reference_id: str | None = None
    payee: Payee | None = None
    description: str | None = None
    shipping: Shipping | None = None
    payments: Payments | None = None
    amount: Amount | None = None
