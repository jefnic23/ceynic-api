from src.database import BaseSchema
from src.models.schemas.paypal.base import Link
from src.models.schemas.paypal.payment_source import PaymentSource


class CreateOrderResponse(BaseSchema):
    id: str
    status: str
    payment_source: PaymentSource | None = None
    links: list[Link]
