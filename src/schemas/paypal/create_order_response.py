from src.database import BaseSchema
from src.schemas.paypal.base import Link
from src.schemas.paypal.payment_source import PaymentSource


class CreateOrderResponse(BaseSchema):
    id: str
    status: str
    payment_source: PaymentSource | None = None
    links: list[Link]
