from datetime import datetime
from src.database import BaseSchema
from src.models.schemas.paypal.base import Link
from src.models.schemas.paypal.payer import Payer
from src.models.schemas.paypal.payment_source import PaymentSource
from src.models.schemas.paypal.purchase_unit import PurchaseUnit


class OrderDetails(BaseSchema):
    id: str
    status: str
    intent: str
    payment_source: PaymentSource
    purchase_units: list[PurchaseUnit]
    payer: Payer
    create_time: datetime
    links: list[Link]
