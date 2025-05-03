from src.database import BaseSchema
from src.models.schemas.paypal.paypal import Paypal


class PaymentSource(BaseSchema):
    paypal: Paypal
