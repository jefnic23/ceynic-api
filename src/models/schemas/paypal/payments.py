from datetime import datetime
from src.database import BaseSchema
from src.models.schemas.paypal.base import Amount, Link, SellerProtection
from src.models.schemas.paypal.seller_receivable_breakdown import SellerReceivableBreakdown


class Authorization(BaseSchema):
    id: str
    status: str
    amount: Amount
    seller_protection: SellerProtection
    expiration_time: datetime
    create_time: datetime
    update_time: datetime
    links: list[Link]


class Capture(BaseSchema):
    id: str
    status: str
    amount: Amount
    seller_protection: SellerProtection
    final_capture: bool
    disbursement_mode: str | None = None
    seller_receivable_breakdown: SellerReceivableBreakdown
    create_time: datetime
    update_time: datetime
    links: list[Link]


class Payments(BaseSchema):
    authorizations: list[Authorization] | None = None
    captures: list[Capture] | None = None
