from src.database import BaseSchema
from src.models.schemas.paypal.base import Tax, UnitAmount


class CustomAmount(BaseSchema):
    label: str
    amount: UnitAmount


class ShippingAmount(BaseSchema):
    amount: UnitAmount
    tax: Tax | None = None


class InvoiceDiscount(BaseSchema):
    percent: str | None = None


class DiscountBreakdown(BaseSchema):
    invoice_discount: InvoiceDiscount | None = None


class AmountBreakdown(BaseSchema):
    custom: CustomAmount | None = None
    shipping: ShippingAmount | None = None
    discount: DiscountBreakdown | None = None


class Amount(BaseSchema):
    breakdown: AmountBreakdown
