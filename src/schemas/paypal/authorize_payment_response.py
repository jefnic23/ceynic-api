from datetime import datetime, timedelta
from src.database import BaseSchema
from src.schemas.paypal.base import Link
from src.schemas.paypal.payer import Payer
from src.schemas.paypal.payment_source import PaymentSource
from src.schemas.paypal.purchase_unit import PurchaseUnit


class AuthorizePaymentResponse(BaseSchema):
    id: str
    status: str
    payment_source: PaymentSource
    purchase_units: list[PurchaseUnit]
    payer: Payer
    links: list[Link]

    @property
    def authorization_id(self) -> str:
        return self.purchase_units[0].payments.authorizations[0].id

    @property
    def create_time(self) -> datetime:
        return self.purchase_units[0].payments.authorizations[0].create_time
