from src.database import BaseSchema
from src.models.schemas.paypal.base import UnitAmount


class PartialPayment(BaseSchema):
    allow_partial_payment: bool
    minimum_amount_due: UnitAmount


class Configuration(BaseSchema):
    partial_payment: PartialPayment | None = None
    allow_tip: bool
    tax_calculated_after_discount: bool
    tax_inclusive: bool
    template_id: str
