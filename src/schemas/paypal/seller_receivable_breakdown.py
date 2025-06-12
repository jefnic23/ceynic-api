from src.schemas.base import BaseSchema
from src.schemas.paypal.base import GrossAmount, NetAmount, PaypalFee


class SellerReceivableBreakdown(BaseSchema):
    gross_amount: GrossAmount
    paypal_fee: PaypalFee
    net_amount: NetAmount
