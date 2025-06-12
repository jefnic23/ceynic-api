from datetime import datetime

from src.schemas.base import BaseSchema
from src.schemas.paypal.base import UnitAmount, Link, SellerProtection
from src.schemas.paypal.seller_receivable_breakdown import SellerReceivableBreakdown


class Authorization(BaseSchema):
    id: str
    status: str
    amount: UnitAmount
    seller_protection: SellerProtection
    expiration_time: datetime | None = None
    create_time: datetime | None = None
    update_time: datetime | None = None
    links: list[Link]


class Capture(BaseSchema):
    id: str
    status: str
    amount: UnitAmount
    seller_protection: SellerProtection
    final_capture: bool
    disbursement_mode: str | None = None
    seller_receivable_breakdown: SellerReceivableBreakdown
    create_time: datetime | None = None
    update_time: datetime | None = None
    links: list[Link]


class Payments(BaseSchema):
    authorizations: list[Authorization] | None = None
    captures: list[Capture] | None = None
