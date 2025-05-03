from datetime import datetime
from src.database import BaseSchema
from src.models.schemas.paypal.base import Amount, Link, SellerProtection
from src.models.schemas.paypal.seller_receivable_breakdown import SellerReceivableBreakdown


class CapturePaymentResponse(BaseSchema):
    id: str
    status: str
    final_capture: bool
    amount: Amount
    seller_protection: SellerProtection
    seller_receivable_breakdown: SellerReceivableBreakdown
    create_time: datetime
    update_time: datetime
    invoice_id: str | None = None
    links: list[Link]
