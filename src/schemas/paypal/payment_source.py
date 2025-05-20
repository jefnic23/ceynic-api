from src.database import BaseSchema
from src.schemas.paypal.paypal import Paypal


class PaymentSource(BaseSchema):
    paypal: Paypal
