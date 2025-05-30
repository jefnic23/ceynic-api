from pydantic import BaseModel
from src.schemas.paypal.base import GrossAmount, NetAmount, PaypalFee


class SellerReceivableBreakdown(BaseModel):
    gross_amount: GrossAmount
    paypal_fee: PaypalFee
    net_amount: NetAmount
