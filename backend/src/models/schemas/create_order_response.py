from pydantic import BaseModel

from backend.src.models.schemas.order import Paypal


class Link(BaseModel):
    href: str
    rel: str
    method: str


class PaymentSource(BaseModel):
    paypal: Paypal | None


class CreateOrder(BaseModel):
    id: str
    status: str
    payment_source: PaymentSource | None = None
    links: list[Link]
